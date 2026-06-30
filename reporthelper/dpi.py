from __future__ import annotations

import ctypes


def enable_dpi_awareness() -> None:
    """Ask Windows for real physical pixels instead of scaled coordinates."""

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
