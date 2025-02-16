from __future__ import annotations

from app.ui.context import UIContext
from app.ui.window import MainWindow

context: UIContext | None = None


def create_window(
    app_version: str,
    app_name: str = "App",
    default_theme: str = "dark",
    default_zoom: int = 0,
) -> MainWindow:
    main_window = MainWindow(app_version, app_name, default_theme, default_zoom)

    global context
    if context is None:
        context = UIContext(main_window)

    return main_window


__all__ = ["create_window", "context"]
