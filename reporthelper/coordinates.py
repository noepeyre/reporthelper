from __future__ import annotations

import ctypes
from dataclasses import dataclass

from pynput.mouse import Controller

from .config import AutomationConfig, LayoutReference


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class ScreenSize:
    width: int
    height: int


class CoordinateCalculator:
    def __init__(self, layout: LayoutReference, mouse: Controller | None = None) -> None:
        self._layout = layout
        self._mouse = mouse or Controller()

    def set_layout(self, layout: LayoutReference) -> None:
        self._layout = layout

    def screen_size(self) -> ScreenSize:
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
        return ScreenSize(width=int(width), height=int(height))

    def points_for(self, config: AutomationConfig) -> tuple[Point, Point, Point]:
        config.validate()
        screen = self.screen_size()
        slot_index = config.target_slot - 1
        slot_menu = self._layout.menu_5[slot_index] if config.menu_options == 5 else self._layout.menu_4[slot_index]
        slot = self._ratio_point(screen, slot_menu.slot.x, slot_menu.slot.y)
        option_ratio = slot_menu.option_points[config.selected_option - 1]
        option = self._ratio_point(screen, option_ratio.x, option_ratio.y)
        validation = self._ratio_point(screen, slot_menu.validation.x, slot_menu.validation.y)
        return slot, option, validation

    @staticmethod
    def _ratio_point(screen: ScreenSize, x_ratio: float, y_ratio: float) -> Point:
        return Point(
            x=round(screen.width * x_ratio),
            y=round(screen.height * y_ratio),
        )
