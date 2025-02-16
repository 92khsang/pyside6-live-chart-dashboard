from __future__ import annotations

from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Callable,
    Optional,
)

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import QWidget

from app.core.log import get_logger


class QWidgetABCMeta(type(QWidget), ABCMeta):
    pass


class BaseUI(QWidget, metaclass=QWidgetABCMeta):

    _logger = get_logger(__name__)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    @abstractmethod
    def _setup_ui(self) -> None:
        """
        Abstract method to set up the UI. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def _clear_widget_reference(self) -> None:
        """
        Abstract method to clear the widget reference. Must be implemented by subclasses.
        """
        pass

    def _switch_ui(self, ui_class: Callable[..., "BaseUI"], *args, **kwargs) -> None:
        """
        Switch the UI to the specified class.
        """
        from app.ui import context

        context.switch_ui(ui_class, *args, **kwargs)
        self._clear_widget_reference()

    def _show_error(
        self, title: str, message: str, exception: Optional[Exception] = None
    ) -> None:
        """
        Displays an error message dialog with improved styling.
        """

        self._logger.error(msg=message, exc_info=exception)

        from app.ui.modals.message import ErrorMessageModal

        dialog = ErrorMessageModal(
            title=title, message=message, exception=exception, parent=self
        )
        dialog.exec()

    def _show_warning(self, title: str, message: str) -> None:
        """
        Displays a warning message dialog with improved styling.
        """

        self._logger.warning(msg=message)

        from app.ui.modals.message import WarningMessageModal

        dialog = WarningMessageModal(title=title, message=message, parent=self)
        dialog.exec()

    def _show_info(self, title: str, message: str) -> None:
        """
        Displays an information message dialog with improved styling.
        """

        self._logger.info(msg=message, stacklevel=3)

        from app.ui.modals.message import InfoMessageModal

        dialog = InfoMessageModal(title=title, message=message, parent=self)
        dialog.exec()
