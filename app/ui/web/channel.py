from __future__ import annotations

from typing import (
    Callable,
    TYPE_CHECKING,
)

from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class WebChannelHandler(QObject):
    message_received = Signal(str, str)

    def __init__(
        self,
        message_received: Callable[[str, str], None],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.message_received.connect(message_received)

    @Slot(str, str)
    def sendMessage(self, sender, message):
        self.message_received.emit(sender, message)
