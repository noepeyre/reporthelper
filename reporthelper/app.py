from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from queue import Empty, Queue
from threading import Event, Lock

from .automation import AutomationRunner
from .config import (
    DEFAULT_CONFIG,
    AutomationConfig,
    discover_layout_files,
    layout_path,
    load_layout,
)
from .coordinates import CoordinateCalculator
from .dpi import enable_dpi_awareness
from .hotkeys import HotkeyService
from .mouse_control import MouseActions
from .ui import ConfigDialog


class ReportHelperApp:
    def __init__(self) -> None:
        self._config: AutomationConfig = replace(DEFAULT_CONFIG)
        self._configured_once = False
        self._lock = Lock()
        self._quit_event = Event()
        self._actions: Queue[Callable[[], None]] = Queue()
        self._layout = load_layout(layout_path(self._config.layout_file))
        self._calculator = CoordinateCalculator(self._layout)
        self._runner = AutomationRunner(
            self._calculator,
            MouseActions(),
        )
        self._hotkeys = HotkeyService(
            on_configure=lambda: self._post(self.open_config),
            on_toggle=lambda: self._post(self.toggle_automation),
            on_quit=lambda: self._post(self.quit),
        )

    def run(self) -> None:
        print("Report Helper ready.")
        print("F8: configuration | F10: start/stop | F9: quit")
        self._hotkeys.start()
        while not self._quit_event.is_set():
            try:
                action = self._actions.get(timeout=0.1)
            except Empty:
                continue
            action()
        self._hotkeys.stop()
        self._runner.stop_and_wait()

    def _post(self, action: Callable[[], None]) -> None:
        self._actions.put(action)

    def open_config(self) -> None:
        if self._runner.is_running:
            print("Configuration ignored: automation is running.")
            return
        with self._lock:
            dialog = ConfigDialog(self._config, discover_layout_files())
            result = dialog.show()
            if result is not None:
                self._config = result
                self._layout = load_layout(layout_path(result.layout_file))
                self._calculator.set_layout(self._layout)
                self._configured_once = True
                print(
                    "Configuration saved: "
                    f"slot={result.target_slot}, "
                    f"options={result.menu_options}, "
                    f"selection={result.selected_option}, "
                    f"loops={result.loop_count}, "
                    f"speed={result.speed_ms}ms, "
                    f"offset={result.random_offset_px}px, "
                    f"layout={result.layout_file}"
                )

    def toggle_automation(self) -> None:
        if self._runner.is_running:
            self._runner.stop()
            print("Automation stopped.")
            return
        if not self._configured_once:
            print("Open and save the configuration with F8 before starting.")
            return
        with self._lock:
            self._layout = load_layout(layout_path(self._config.layout_file))
            self._calculator.set_layout(self._layout)
            started = self._runner.start(self._config)
        if started:
            print("Automation started.")

    def quit(self) -> None:
        print("Closing...")
        self._runner.stop()
        self._quit_event.set()


def main() -> None:
    enable_dpi_awareness()
    ReportHelperApp().run()
