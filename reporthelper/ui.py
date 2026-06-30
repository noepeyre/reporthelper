from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .config import AutomationConfig


class ConfigDialog:
    def __init__(self, initial: AutomationConfig, layout_files: tuple[str, ...]) -> None:
        self._initial = initial
        self._layout_files = layout_files
        self.result: AutomationConfig | None = None

    def show(self) -> AutomationConfig | None:
        root = tk.Tk()
        root.title("Report Helper")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        slot_var = tk.IntVar(value=self._initial.target_slot)
        options_var = tk.IntVar(value=self._initial.menu_options)
        selected_var = tk.IntVar(value=self._initial.selected_option)
        loops_var = tk.IntVar(value=self._initial.loop_count)
        speed_var = tk.IntVar(value=self._initial.speed_ms)
        offset_var = tk.IntVar(value=self._initial.random_offset_px)
        layout_var = tk.StringVar(value=self._initial.layout_file)

        frame = ttk.Frame(root, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Target slot").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Spinbox(frame, from_=1, to=10, textvariable=slot_var, width=8).grid(
            row=0, column=1, sticky="ew", pady=4
        )

        ttk.Label(frame, text="Menu options").grid(row=1, column=0, sticky="w", pady=4)
        options_box = ttk.Combobox(
            frame,
            textvariable=options_var,
            values=(4, 5),
            state="readonly",
            width=6,
        )
        options_box.grid(row=1, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Option to select").grid(row=2, column=0, sticky="w", pady=4)
        selected_box = ttk.Combobox(frame, textvariable=selected_var, state="readonly", width=6)
        selected_box.grid(row=2, column=1, sticky="ew", pady=4)

        ttk.Label(frame, text="Loop count (0 = infinite)").grid(
            row=3, column=0, sticky="w", pady=4
        )
        ttk.Spinbox(frame, from_=0, to=999999, textvariable=loops_var, width=8).grid(
            row=3, column=1, sticky="ew", pady=4
        )

        ttk.Label(frame, text="Speed (ms, 0 = maximum)").grid(
            row=4, column=0, sticky="w", pady=4
        )
        ttk.Spinbox(frame, from_=0, to=999999, textvariable=speed_var, width=8).grid(
            row=4, column=1, sticky="ew", pady=4
        )

        ttk.Label(frame, text="Random offset (px)").grid(row=5, column=0, sticky="w", pady=4)
        ttk.Spinbox(frame, from_=0, to=9999, textvariable=offset_var, width=8).grid(
            row=5, column=1, sticky="ew", pady=4
        )

        ttk.Label(frame, text="Layout").grid(row=6, column=0, sticky="w", pady=4)
        layout_box = ttk.Combobox(
            frame,
            textvariable=layout_var,
            values=self._layout_files,
            state="readonly",
            width=24,
        )
        layout_box.grid(row=6, column=1, sticky="ew", pady=4)

        buttons = ttk.Frame(frame)
        buttons.grid(row=7, column=0, columnspan=2, sticky="e", pady=(14, 0))

        def update_selected_options(*_args: object) -> None:
            count = int(options_var.get())
            values = tuple(range(1, count + 1))
            selected_box.configure(values=values)
            if selected_var.get() > count:
                selected_var.set(count)

        def save() -> None:
            config = AutomationConfig(
                target_slot=int(slot_var.get()),
                menu_options=int(options_var.get()),
                selected_option=int(selected_var.get()),
                loop_count=int(loops_var.get()),
                speed_ms=int(speed_var.get()),
                random_offset_px=int(offset_var.get()),
                layout_file=layout_var.get(),
            )
            config.validate()
            self.result = config
            root.destroy()

        def cancel() -> None:
            root.destroy()

        ttk.Button(buttons, text="Cancel", command=cancel).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Save", command=save).grid(row=0, column=1)

        options_var.trace_add("write", update_selected_options)
        update_selected_options()
        root.protocol("WM_DELETE_WINDOW", cancel)
        root.bind("<Return>", lambda _event: save())
        root.bind("<Escape>", lambda _event: cancel())
        root.update_idletasks()

        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 2
        root.geometry(f"+{x}+{y}")
        root.mainloop()
        return self.result
