from __future__ import annotations

import logging
from typing import override

from PySide6.QtCore import QEvent
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    Qt,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
)
from qt_stylehelper import DynamicQtStyleTools

from app.core.log import get_logger


class MainWindow(QMainWindow):
    """
    Main application window managing themes and zoom functionality.
    """

    _logger = get_logger(__name__)

    THEME_LIST: list[str] = [
        "dark",
        "light",
        "dark_blue",
        "dark_cyan",
        "dark_amber",
        "light_pink",
        "light_teal",
        "light_amber",
    ]

    ZOOM_RANGE: range = range(-2, 3)

    def __init__(
        self,
        app_version: str,
        app_name: str = "App",
        default_theme: str = "dark",
        default_zoom: int = 0,
    ):
        super().__init__()

        if default_theme not in self.THEME_LIST:
            self._logger.warning(
                f"Theme '{default_theme}' not found in theme list, defaulting to 'dark'"
            )
            default_theme = "dark"

        if default_zoom not in self.ZOOM_RANGE:
            self._logger.warning(
                f"Zoom '{default_zoom}' not found in zoom range, defaulting to '0'"
            )
            default_zoom = 0

        logging.debug(
            f"initial values: {app_name}, {app_version}, {default_theme}, {default_zoom}"
        )

        style_tools = DynamicQtStyleTools(app_name)
        style_tools.set_extra({"density_scale": str(default_zoom)})
        style_tools.apply_stylesheet(self, self._convert_theme_name(default_theme))
        self._style_tools = style_tools

        self.setWindowTitle(f"{app_name} ({app_version})")
        self._setup_menu()

    def set_central_widget(self, widget: QWidget):
        """
        Set the central widget of the main window, update the UI,
        and adjust the window size accordingly.

        Args:
            widget (QWidget): The widget to set as the central widget.
        """
        self.setCentralWidget(widget)
        self.update()
        self._adjust_size()

    @override
    def changeEvent(self, event: QEvent):
        """Detect window state changes and run adjustSize conditionally."""
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() in {
                Qt.WindowState.WindowNoState,
                Qt.WindowState.WindowMinimized,
            }:
                self.adjustSize()
        super().changeEvent(event)

    def _adjust_size(self):
        current_state = self.windowState()
        if current_state == Qt.WindowState.WindowNoState:
            self.adjustSize()
        self.setWindowState(current_state)

    def _setup_menu(self) -> None:
        self._setup_theme_menu()
        self._setup_zoom_menu()

    def _setup_theme_menu(self) -> None:
        theme_menu = self.menuBar().addMenu("Theme")
        theme_action_group = QActionGroup(theme_menu)
        theme_action_group.setExclusive(True)

        for style_name in self.THEME_LIST:
            action = QAction(style_name, theme_action_group)
            action.triggered.connect(
                lambda _, style=style_name: self._style_tools.apply_stylesheet(
                    self, self._convert_theme_name(style)
                )
            )
            theme_menu.addAction(action)

    def _setup_zoom_menu(self) -> None:
        zoom_menu = self.menuBar().addMenu("Zoom")
        zoom_action_group = QActionGroup(zoom_menu)
        zoom_action_group.setExclusive(True)

        for zoom in self.ZOOM_RANGE:
            action = QAction(str(zoom), zoom_action_group)
            action.triggered.connect(
                lambda _, zoom_scale=zoom: self._update_zoom(zoom_scale)
            )
            zoom_menu.addAction(action)

    def _update_zoom(self, zoom_scale: str):
        if hasattr(self._style_tools, "set_extra"):
            self._style_tools.set_extra({"density_scale": zoom_scale})
        self._style_tools.refresh_stylesheet(self)
        self._adjust_size()

    @staticmethod
    def _convert_theme_name(theme_name: str) -> str:
        if theme_name == "dark":
            return "dark_pink"
        elif theme_name == "light":
            return "light_cyan_500"
        else:
            return theme_name
