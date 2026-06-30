from __future__ import annotations

import random
import time
from threading import Event

from pynput.mouse import Button, Controller

from .coordinates import Point


class MouseActions:
    def __init__(
        self,
        mouse: Controller | None = None,
    ) -> None:
        self._mouse = mouse or Controller()

    def move_and_click(
        self,
        point: Point,
        stop_event: Event,
        speed_ms: int = 0,
        random_offset_px: int = 0,
    ) -> bool:
        if stop_event.is_set():
            return False
        target = self._with_random_offset(point, random_offset_px)
        self._mouse.position = (target.x, target.y)
        if stop_event.is_set():
            return False
        self._mouse.click(Button.left, 1)
        if speed_ms:
            time.sleep(speed_ms / 1000)
        return not stop_event.is_set()

    @staticmethod
    def _with_random_offset(point: Point, random_offset_px: int) -> Point:
        if random_offset_px <= 0:
            return point
        return Point(
            x=point.x + random.randint(-random_offset_px, random_offset_px),
            y=point.y + random.randint(-random_offset_px, random_offset_px),
        )
