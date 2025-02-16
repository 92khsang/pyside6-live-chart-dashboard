from __future__ import annotations

import gc
import threading
from typing import (
    Callable,
    Optional,
    TYPE_CHECKING,
    TypeVar,
)

from PySide6.QtWidgets import (
    QWidget,
)

from app.core.log import get_logger
from app.decorators import (
    lock_methods,
    singleton,
)

UI = TypeVar("UI")

if TYPE_CHECKING:
    from logging import Logger
    from app.ui.pages.base import BaseUI
    from app.ui.window import MainWindow


@singleton
@lock_methods
class UIContext:
    _lock: threading.RLock = threading.RLock()
    _logger: Logger = get_logger(__name__)

    def __init__(self, main_window: MainWindow):
        self._main_window = main_window
        self._current_ui: Optional[BaseUI] = None

    def show_ui(self):
        """
        Shows the main window with the current UI.

        This method is useful for when the application is already initialized and
        the UI context is already set up. It will show the main window with the
        current UI.
        """
        self._main_window.show()

    def switch_ui(self, new_ui_class: Callable[..., BaseUI], *args, **kwargs) -> None:
        """
        Switch the UI to the specified class.

        Args:
            new_ui_class: The UI class to switch to.
            *args: Additional positional arguments to pass to the UI class.
            **kwargs: Additional keyword arguments to pass to the UI class.

        Raises:
            ValueError: If new_ui_class is None.

        """
        if new_ui_class is None:
            raise ValueError("new_ui_class cannot be None")

        self._delete_current_ui()

        new_args = (self._main_window,) + args
        self._current_ui = new_ui_class(*new_args, **kwargs)
        self._main_window.set_central_widget(self._current_ui)

        self._logger.debug("Switched to UI... %s", self._current_ui.__class__.__name__)

    def _delete_current_ui(self) -> None:
        if self._current_ui:
            self._logger.debug(
                "Closing the current UI... %s", self._current_ui.__class__.__name__
            )
            self._delete_referenced_widgets()
            self._current_ui.setParent(None)
            self._current_ui.deleteLater()
            self._current_ui = None
            self._run_gc()

    def _delete_referenced_widgets(self) -> None:
        for referent in gc.get_referents(self._current_ui):
            if isinstance(referent, QWidget):
                self._logger.debug(
                    "Deleting referenced widget... %s", referent.__class__.__name__
                )
                referent.deleteLater()

    def _run_gc(self) -> None:
        gc.collect()
        gc_stats = gc.get_stats()
        self._logger.debug(f"GC collected objects and stats: {gc_stats}")
