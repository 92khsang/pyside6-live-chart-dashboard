from __future__ import annotations

import logging
from pathlib import Path
from typing import (
    Any,
    TYPE_CHECKING,
)

from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout

from app.core.log import get_logger
from app.ui.pages.base import BaseUI
from app.ui.web.channel import WebChannelHandler

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class WebEnginePageWrapper(QWebEnginePage):
    _logger = get_logger(__name__)

    def javaScriptConsoleMessage(
        self, level: Any, message: str, lineNumber: int, sourceID: str
    ) -> None:
        super().javaScriptConsoleMessage(level, message, lineNumber, sourceID)
        level_mapping = {
            0: logging.DEBUG,
            1: logging.WARNING,
            2: logging.ERROR,
            3: logging.CRITICAL,
        }

        system_log_level = logging.getLogger().level
        console_log_level = level_mapping.get(level.value, system_log_level)
        if console_log_level >= system_log_level:
            self._logger.log(
                console_log_level,
                f"JS Console [{logging.getLevelName(console_log_level)}]: {message} (Line {lineNumber})",
            )


class WorkspaceUI(BaseUI):
    _logger = get_logger(__name__)

    if TYPE_CHECKING:
        editor_view: QWebEngineView | None
        editor_web_channel: QWebChannel | None
        editor_web_channel_handler: WebChannelHandler | None

    def __init__(self, parent: QWidget, editor_html: Path | str):
        super().__init__(parent)

        editor_html = Path(editor_html)
        if not editor_html.is_file() and editor_html.suffix != ".html":
            raise ValueError(f"Invalid editor HTML file: {editor_html}")

        self.file_url: str = editor_html.resolve().as_uri()

        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout: QVBoxLayout = QVBoxLayout()

        editor_view = QWebEngineView()
        editor_page = WebEnginePageWrapper(self)
        editor_view.setPage(editor_page)
        editor_view.setUrl(self.file_url)
        main_layout.addWidget(editor_view)

        editor_web_channel = QWebChannel(self)
        editor_web_channel_handler = WebChannelHandler(self.process_message, self)
        editor_web_channel.registerObject("handler", editor_web_channel_handler)

        editor_page.setWebChannel(editor_web_channel)

        self.editor_view = editor_view
        self.setLayout(main_layout)

    def process_message(self, sender: str, message: str) -> None:
        self._logger.debug(f"Message from {sender}: {message}")
        # Dispatch event in JavaScript only if the frontend is listening
        js_script = f"""
            document.dispatchEvent(new CustomEvent('webChannelMessage', {{
                detail: {{ channelName: "{sender}", message: "{message}" }}
            }}));
        """
        self.editor_view.page().runJavaScript(js_script)

    def _clear_widget_reference(self) -> None:
        self.editor_view = None
