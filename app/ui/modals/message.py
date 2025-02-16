from __future__ import annotations

from typing import (
    Optional,
    override,
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStyle,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.ui.utils import calculate_size_from_font


class _BaseMessageModal(QDialog):
    def __init__(self, parent: QWidget, emoji: str, title: str, message: str):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle(title)

        self._setup_min_size(parent)
        self._setup_default_ui(emoji, message)

    def _setup_min_size(self, parent: QWidget):
        parent_size = parent.sizeHint()
        self.setMinimumSize((parent_size.width() // 2), (parent_size.height() // 3))

    def _setup_default_ui(self, emoji: str, message: str):
        main_layout = QVBoxLayout(self)

        self._setup_labels(main_layout, emoji, message)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        self._create_bottom_button(button_layout)

        self.setLayout(main_layout)

    def _setup_labels(self, main_layout: QVBoxLayout, emoji: str, message: str):
        label_layout = QHBoxLayout()
        icon_label = QLabel(parent=self, text=emoji)
        icon_label.setWordWrap(True)
        icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.update_font_size(icon_label)
        label_layout.addWidget(icon_label)

        message_label = QLabel(message, self)
        message_label.setWordWrap(True)
        message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        label_layout.addWidget(message_label)
        main_layout.addLayout(label_layout)

    def update_font_size(self, label):
        shorter_side = min(self.size().width(), self.size().height())

        font_size = shorter_side // 6

        label.setStyleSheet(f"font-size: {font_size}px;")

        square_size = font_size * 2
        label.setFixedSize(square_size, square_size)

    def _create_bottom_button(self, button_layout: QHBoxLayout) -> None:
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, self)
        button_box.accepted.connect(self.accept)
        button_layout.addWidget(button_box)


class InfoMessageModal(_BaseMessageModal):
    def __init__(self, parent: QWidget, title: str, message: str):
        super().__init__(parent, "💡", title, message)


class WarningMessageModal(_BaseMessageModal):
    def __init__(self, parent: QWidget, title: str, message: str):
        super().__init__(parent, "⚠️", title, message)


class ErrorMessageModal(_BaseMessageModal):
    def __init__(
        self,
        parent: QWidget,
        title: str,
        message: str,
        exception: Optional[Exception] = None,
    ):
        self._exception = exception
        super().__init__(parent, "🚨", title, message)

    @override
    def _setup_min_size(self, parent: QWidget):
        parent_size = parent.sizeHint()
        self.setMinimumSize(
            max(((parent_size.width() * 2) // 3), 300),
            max(((parent_size.height() * 2) // 3), 150),
        )

    def _create_bottom_button(self, button_layout: QHBoxLayout):
        # Add stretch for alignment
        button_layout.addStretch(1)

        if self._exception:
            import traceback

            detailed_text = "".join(
                traceback.format_exception(
                    None, self._exception, self._exception.__traceback__
                )
            )
            texts: list[str] = detailed_text.splitlines()
            total_lines = len(texts) + 4
            longest_text = max(texts, key=len)

            self.detailed_text_edit = QTextEdit(self)
            self.detailed_text_edit.setReadOnly(True)
            self.detailed_text_edit.setText(detailed_text)
            self.detailed_text_edit.setVisible(False)

            msg_base_size = calculate_size_from_font(
                longest_text, self.detailed_text_edit.font()
            )
            self.setMinimumWidth(msg_base_size.width() // 2)
            self.detailed_text_edit.setMaximumHeight(
                msg_base_size.height() * (total_lines * 2)
            )
            self.layout().addWidget(self.detailed_text_edit)

            detail_button = QPushButton(
                self.style().standardIcon(
                    QStyle.StandardPixmap.SP_FileDialogDetailedView
                ),
                "Details",
                self,
            )
            detail_button.clicked.connect(self._toggle_details)
            button_layout.addWidget(detail_button)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, self)
        button_box.accepted.connect(self.accept)

        button_layout.addWidget(button_box)

    def _toggle_details(self):
        """Toggles the visibility of the detailed exception text."""
        if self.detailed_text_edit.isVisible():
            self.detailed_text_edit.setVisible(False)
            self.adjustSize()
        else:
            self.detailed_text_edit.setVisible(True)
            self.adjustSize()


__all__ = ["InfoMessageModal", "WarningMessageModal", "ErrorMessageModal"]
