from __future__ import annotations

import ctypes
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from queue import Empty, Queue
from tkinter import messagebox, ttk

from pynput import keyboard
from pynput.mouse import Controller

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from reporthelper.config import (
        LAYOUT_FILE,
        LayoutReference,
        RatioPoint,
        SlotMenuReference,
        save_layout,
    )
    from reporthelper.dpi import enable_dpi_awareness
else:
    from .config import (
        LAYOUT_FILE,
        LayoutReference,
        RatioPoint,
        SlotMenuReference,
        save_layout,
    )
    from .dpi import enable_dpi_awareness


@dataclass(frozen=True, slots=True)
class CaptureStep:
    key: str
    board: str
    title: str
    instruction: str


class LayoutSetupApp:
    def __init__(self) -> None:
        self._mouse = Controller()
        self._captures: dict[str, tuple[int, int]] = {}
        self._index = 0
        self._closed = False
        self._steps: tuple[CaptureStep, ...] = ()
        self._queue: Queue[str] = Queue()
        self._listener = keyboard.GlobalHotKeys(
            {
                "<f7>": lambda: self._queue.put("capture"),
                "<f9>": lambda: self._queue.put("quit"),
            }
        )

        self._root = tk.Tk()
        self._root.title("Report Helper Setup")
        self._root.resizable(False, False)
        self._root.attributes("-topmost", True)

        self._frame = ttk.Frame(self._root, padding=16)
        self._frame.grid(row=0, column=0, sticky="nsew")

        self._current_var = tk.StringVar(value="top")
        self._progress = ttk.Label(self._frame)
        self._title = ttk.Label(self._frame, font=("", 12, "bold"))
        self._instruction = ttk.Label(self._frame, wraplength=520, justify="left")
        self._last_capture = ttk.Label(self._frame)

        self._show_start()
        self._center()

    def run(self) -> None:
        self._listener.start()
        self._root.after(80, self._poll_queue)
        self._root.mainloop()
        self._listener.stop()

    def _show_start(self) -> None:
        self._clear_frame()
        ttk.Label(self._frame, text="Starting current").grid(row=0, column=0, sticky="w", pady=4)
        current_box = ttk.Combobox(
            self._frame,
            textvariable=self._current_var,
            values=("top", "bottom"),
            state="readonly",
            width=10,
        )
        current_box.grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(self._frame, text="Start", command=self._start_steps).grid(
            row=1, column=0, columnspan=2, sticky="e", pady=(14, 0)
        )

    def _start_steps(self) -> None:
        self._steps = self._build_steps(self._current_var.get())
        self._index = 0
        self._captures.clear()
        self._clear_frame()

        self._progress.grid(row=0, column=0, sticky="w")
        self._title.grid(row=1, column=0, sticky="w", pady=(10, 4))
        self._instruction.grid(row=2, column=0, sticky="w")
        self._last_capture.grid(row=3, column=0, sticky="w", pady=(10, 0))

        buttons = ttk.Frame(self._frame)
        buttons.grid(row=4, column=0, sticky="e", pady=(14, 0))
        ttk.Button(buttons, text="Back", command=self._back).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Capture F7", command=self._capture).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(buttons, text="Quit F9", command=self._quit).grid(row=0, column=2)

        self._refresh()
        self._center()

    def _build_steps(self, current: str) -> tuple[CaptureStep, ...]:
        if current == "top":
            phases = (
                ("top", ((range(1, 6), 5), (range(6, 11), 4))),
                ("bottom", ((range(1, 6), 4), (range(6, 11), 5))),
            )
        else:
            phases = (
                ("bottom", ((range(1, 6), 4), (range(6, 11), 5))),
                ("top", ((range(1, 6), 5), (range(6, 11), 4))),
            )

        steps: list[CaptureStep] = []
        for board, groups in phases:
            steps.extend(self._slot_steps(board))
            for slots, menu_count in groups:
                steps.extend(self._menu_steps(board, slots, menu_count))
                steps.extend(self._validation_steps(board, slots, menu_count))
        return tuple(steps)

    @staticmethod
    def _slot_steps(board: str) -> list[CaptureStep]:
        return [
            CaptureStep(
                key=f"{board}:slot:{slot}",
                board=board,
                title=f"{board} - slot {slot} button",
                instruction=f"Place the mouse on the button for slot {slot}.",
            )
            for slot in range(1, 11)
        ]

    @staticmethod
    def _menu_steps(board: str, slots: range, menu_count: int) -> list[CaptureStep]:
        return [
            CaptureStep(
                key=f"{board}:slot:{slot}:menu:{menu_count}:option:{option}",
                board=board,
                title=f"{board} - slot {slot} - menu {menu_count} - option {option}",
                instruction=(
                    f"Open the {menu_count}-option menu for slot {slot}, then place the mouse "
                    f"on option {option}."
                ),
            )
            for slot in slots
            for option in range(1, menu_count + 1)
        ]

    @staticmethod
    def _validation_steps(board: str, slots: range, menu_count: int) -> list[CaptureStep]:
        return [
            CaptureStep(
                key=f"{board}:slot:{slot}:menu:{menu_count}:validation",
                board=board,
                title=f"{board} - slot {slot} - menu {menu_count} confirmation",
                instruction=f"Place the mouse on the confirmation button for slot {slot}.",
            )
            for slot in slots
        ]

    def _poll_queue(self) -> None:
        if self._closed:
            return
        while True:
            try:
                action = self._queue.get_nowait()
            except Empty:
                break
            if action == "capture":
                self._capture()
            elif action == "quit":
                self._quit()
        if not self._closed:
            self._root.after(80, self._poll_queue)

    def _capture(self) -> None:
        if not self._steps or self._index >= len(self._steps):
            return
        x, y = self._mouse.position
        step = self._steps[self._index]
        self._captures[step.key] = (int(x), int(y))
        self._last_capture.configure(text=f"Last capture: x={int(x)}, y={int(y)}")
        self._index += 1
        if self._index == len(self._steps):
            self._save()
            return
        self._refresh()

    def _back(self) -> None:
        if self._index <= 0:
            return
        self._index -= 1
        self._captures.pop(self._steps[self._index].key, None)
        self._refresh()

    def _save(self) -> None:
        save_layout(self._build_layout())
        messagebox.showinfo(
            "Configuration complete",
            f"Ratios saved to:\n{LAYOUT_FILE}",
        )
        self._quit()

    def _build_layout(self) -> LayoutReference:
        return LayoutReference(
            menu_4=tuple(self._slot_menu(slot, 4) for slot in range(1, 11)),
            menu_5=tuple(self._slot_menu(slot, 5) for slot in range(1, 11)),
        )

    def _slot_menu(self, slot: int, menu_count: int) -> SlotMenuReference:
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
        board = self._captured_board_for(slot, menu_count)
        prefix = f"{board}:slot:{slot}:menu:{menu_count}"
        return SlotMenuReference(
            slot=self._ratio_point(self._captures[f"{board}:slot:{slot}"], width, height),
            option_points=tuple(
                self._ratio_point(self._captures[f"{prefix}:option:{option}"], width, height)
                for option in range(1, menu_count + 1)
            ),
            validation=self._ratio_point(self._captures[f"{prefix}:validation"], width, height),
        )

    def _captured_board_for(self, slot: int, menu_count: int) -> str:
        for board in ("top", "bottom"):
            if f"{board}:slot:{slot}:menu:{menu_count}:option:1" in self._captures:
                return board
        raise KeyError(f"missing capture for slot {slot}, menu {menu_count}")

    @staticmethod
    def _ratio_point(point: tuple[int, int], width: int, height: int) -> RatioPoint:
        return RatioPoint(point[0] / width, point[1] / height)

    def _refresh(self) -> None:
        step = self._steps[self._index]
        self._progress.configure(text=f"Step {self._index + 1}/{len(self._steps)}")
        self._title.configure(text=step.title)
        self._instruction.configure(text=step.instruction)
        self._last_capture.configure(text="Press F7 to capture the current position.")

    def _center(self) -> None:
        self._root.update_idletasks()
        width = self._root.winfo_width()
        height = self._root.winfo_height()
        x = (self._root.winfo_screenwidth() - width) // 2
        y = (self._root.winfo_screenheight() - height) // 2
        self._root.geometry(f"+{x}+{y}")

    def _clear_frame(self) -> None:
        for child in self._frame.winfo_children():
            child.grid_forget()

    def _quit(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._root.destroy()


def main() -> None:
    enable_dpi_awareness()
    LayoutSetupApp().run()
