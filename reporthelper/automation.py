from __future__ import annotations

from dataclasses import replace
from threading import Event, Lock, Thread

from .config import AutomationConfig
from .coordinates import CoordinateCalculator
from .mouse_control import MouseActions


class AutomationRunner:
    def __init__(
        self,
        calculator: CoordinateCalculator,
        mouse_actions: MouseActions,
    ) -> None:
        self._calculator = calculator
        self._mouse_actions = mouse_actions
        self._lock = Lock()
        self._stop_event = Event()
        self._thread: Thread | None = None

    @property
    def is_running(self) -> bool:
        thread = self._thread
        return thread is not None and thread.is_alive()

    def start(self, config: AutomationConfig) -> bool:
        with self._lock:
            if self.is_running:
                return False
            self._stop_event.clear()
            run_config = replace(config)
            self._thread = Thread(
                target=self._run,
                args=(run_config,),
                name="reporthelper-automation",
                daemon=True,
            )
            self._thread.start()
            return True

    def stop(self) -> None:
        self._stop_event.set()

    def stop_and_wait(self, timeout: float = 1.5) -> None:
        self.stop()
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=timeout)

    def _run(self, config: AutomationConfig) -> None:
        completed = 0
        while not self._stop_event.is_set():
            if config.loop_count and completed >= config.loop_count:
                break
            slot, option, validation = self._calculator.points_for(config)
            for point in (slot, option, validation):
                if not self._mouse_actions.move_and_click(
                    point,
                    self._stop_event,
                    speed_ms=config.speed_ms,
                    random_offset_px=config.random_offset_px,
                ):
                    return
            completed += 1
