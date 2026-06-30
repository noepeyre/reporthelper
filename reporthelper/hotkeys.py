from __future__ import annotations

from collections.abc import Callable

from pynput import keyboard


class HotkeyService:
    def __init__(
        self,
        on_configure: Callable[[], None],
        on_toggle: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        self._listener = keyboard.GlobalHotKeys(
            {
                "<f8>": on_configure,
                "<f10>": on_toggle,
                "<f9>": on_quit,
            }
        )

    def start(self) -> None:
        self._listener.start()

    def wait(self) -> None:
        self._listener.join()

    def stop(self) -> None:
        self._listener.stop()
