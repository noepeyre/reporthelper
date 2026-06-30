from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class AutomationConfig:
    target_slot: int = 1
    menu_options: int = 4
    selected_option: int = 2
    loop_count: int = 0
    speed_ms: int = 500
    random_offset_px: int = 10
    layout_file: str = "layout_reference_v2.json"

    def validate(self) -> None:
        if not 1 <= self.target_slot <= 10:
            raise ValueError("target_slot must be between 1 and 10")
        if self.menu_options not in (4, 5):
            raise ValueError("menu_options must be 4 or 5")
        if not 1 <= self.selected_option <= self.menu_options:
            raise ValueError("selected_option must fit the menu option count")
        if self.loop_count < 0:
            raise ValueError("loop_count must be positive, or 0 for infinite")
        if self.speed_ms < 0:
            raise ValueError("speed_ms must be 0 or greater")
        if self.random_offset_px < 0:
            raise ValueError("random_offset_px must be 0 or greater")
        if not self.layout_file:
            raise ValueError("layout_file must not be empty")


@dataclass(frozen=True, slots=True)
class RatioPoint:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class SlotMenuReference:
    slot: RatioPoint
    option_points: tuple[RatioPoint, ...]
    validation: RatioPoint


@dataclass(frozen=True, slots=True)
class LayoutReference:
    menu_4: tuple[SlotMenuReference, ...]
    menu_5: tuple[SlotMenuReference, ...]


DEFAULT_CONFIG = AutomationConfig()
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAYOUT_FILE = PROJECT_ROOT / "layout_reference.json"


def _default_slots() -> tuple[RatioPoint, ...]:
    return tuple(RatioPoint(0.44, 0.285 + (index * 0.052)) for index in range(10))


def _slot_menus_from_offsets(
    offsets: tuple[RatioPoint, ...],
    validation: RatioPoint,
    slots: tuple[RatioPoint, ...],
) -> tuple[SlotMenuReference, ...]:
    return tuple(
        SlotMenuReference(
            slot=slot,
            option_points=tuple(
                RatioPoint(slot.x + offset.x, slot.y + offset.y) for offset in offsets
            ),
            validation=validation,
        )
        for slot in slots
    )


def _default_layout() -> LayoutReference:
    slots = _default_slots()
    validation = RatioPoint(0.735, 0.83)
    menu_4_offsets = (
        RatioPoint(0.135, 0.018),
        RatioPoint(0.135, 0.055),
        RatioPoint(0.135, 0.092),
        RatioPoint(0.135, 0.129),
    )
    menu_5_offsets = (*menu_4_offsets, RatioPoint(0.135, 0.166))
    return LayoutReference(
        menu_4=_slot_menus_from_offsets(menu_4_offsets, validation, slots),
        menu_5=_slot_menus_from_offsets(menu_5_offsets, validation, slots),
    )


DEFAULT_LAYOUT = _default_layout()


def load_layout(path: Path = LAYOUT_FILE) -> LayoutReference:
    if not path.exists():
        return DEFAULT_LAYOUT
    data = json.loads(path.read_text(encoding="utf-8"))
    if (
        isinstance(data.get("menu_4"), list)
        and data["menu_4"]
        and "slot" in data["menu_4"][0]
    ):
        return LayoutReference(
            menu_4=_slot_menus(data["menu_4"]),
            menu_5=_slot_menus(data["menu_5"]),
        )
    if "top" in data and "bottom" in data:
        return _layout_from_previous_setup(data)
    if "slots" in data:
        return _single_board_layout_from_data(data)
    return _legacy_layout_from_data(data)


def layout_path(layout_file: str) -> Path:
    return PROJECT_ROOT / Path(layout_file).name


def discover_layout_files() -> tuple[str, ...]:
    files = sorted(path.name for path in PROJECT_ROOT.glob("layout_reference*.json"))
    if "layout_reference.json" not in files:
        files.insert(0, "layout_reference.json")
    return tuple(files)


def save_layout(layout: LayoutReference, path: Path = LAYOUT_FILE) -> None:
    path.write_text(
        json.dumps(asdict(layout), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _layout_from_previous_setup(data: dict[str, Any]) -> LayoutReference:
    top = data["top"]
    bottom = data["bottom"]
    return LayoutReference(
        menu_4=_merge_menu_from_boards(top, bottom, "menu_4"),
        menu_5=_merge_menu_from_boards(top, bottom, "menu_5"),
    )


def _merge_menu_from_boards(
    first: dict[str, Any],
    second: dict[str, Any],
    menu_key: str,
) -> tuple[SlotMenuReference, ...]:
    merged: list[SlotMenuReference] = []
    for index in range(10):
        source = first if _has_real_menu(first, menu_key, index) else second
        menu = source[menu_key][index]
        merged.append(
            SlotMenuReference(
                slot=_point(source["slots"][index]),
                option_points=_points(menu["option_points"]),
                validation=_point(menu["validation"]),
            )
        )
    return tuple(merged)


def _has_real_menu(board: dict[str, Any], menu_key: str, index: int) -> bool:
    return menu_key in board and index < len(board[menu_key]) and bool(board[menu_key][index])


def _single_board_layout_from_data(data: dict[str, Any]) -> LayoutReference:
    slots = _points(data["slots"])
    validation = RatioPoint(float(data.get("validation_x", 0.735)), float(data.get("validation_y", 0.83)))
    return LayoutReference(
        menu_4=_slot_menus_from_offsets(_points(data["menu_4"]["option_offsets"]), validation, slots),
        menu_5=_slot_menus_from_offsets(_points(data["menu_5"]["option_offsets"]), validation, slots),
    )


def _legacy_layout_from_data(data: dict[str, Any]) -> LayoutReference:
    slot_x = float(data.get("slot_x", 0.44))
    first_slot_y = float(data.get("first_slot_y", 0.285))
    slot_gap_y = float(data.get("slot_gap_y", 0.052))
    menu_x_offset = float(data.get("menu_x_offset", 0.135))
    menu_first_option_y_offset = float(data.get("menu_first_option_y_offset", 0.018))
    menu_option_gap_y = float(data.get("menu_option_gap_y", 0.037))
    validation = RatioPoint(
        float(data.get("validation_x", 0.735)),
        float(data.get("validation_y", 0.83)),
    )
    slots = tuple(
        RatioPoint(slot_x, first_slot_y + ((slot - 1) * slot_gap_y))
        for slot in range(1, 11)
    )
    return LayoutReference(
        menu_4=_slot_menus_from_offsets(
            tuple(
                RatioPoint(menu_x_offset, menu_first_option_y_offset + (index * menu_option_gap_y))
                for index in range(4)
            ),
            validation,
            slots,
        ),
        menu_5=_slot_menus_from_offsets(
            tuple(
                RatioPoint(menu_x_offset, menu_first_option_y_offset + (index * menu_option_gap_y))
                for index in range(5)
            ),
            validation,
            slots,
        ),
    )


def _slot_menus(values: list[dict[str, Any]]) -> tuple[SlotMenuReference, ...]:
    return tuple(
        SlotMenuReference(
            slot=_point(value["slot"]),
            option_points=_points(value["option_points"]),
            validation=_point(value["validation"]),
        )
        for value in values
    )


def _points(values: list[dict[str, Any]]) -> tuple[RatioPoint, ...]:
    return tuple(_point(value) for value in values)


def _point(value: dict[str, Any]) -> RatioPoint:
    return RatioPoint(float(value["x"]), float(value["y"]))
