from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout

from app.ui.pages.base import BaseUI

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class WorkspaceUI(BaseUI):
    if TYPE_CHECKING:
        editor_view: QWebEngineView | None

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
        editor_view.setUrl(self.file_url)

        main_layout.addWidget(editor_view)

        self.editor_view = editor_view
        self.setLayout(main_layout)

    def _clear_widget_reference(self) -> None:
        self.editor_view = None
