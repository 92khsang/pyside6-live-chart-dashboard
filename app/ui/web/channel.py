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
    receive_channel = Signal(str, str)
    send_channel = Signal(str, str)

    def __init__(
        self,
        receive_channel: Callable[[str, str], None],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.receive_channel.connect(receive_channel)

    @Slot("QVariant")
    def setup_translate_py2js(self, callback: Callable[[str, str], None]):
        self.send_channel.connect(callback)

    def translate_py2js(self, sender, message):
        self.send_channel.emit(sender, message)

    @Slot(str, str)
    def translate_js2py(self, sender, message):
        self.receive_channel.emit(sender, message)
