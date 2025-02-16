from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPoint
from PySide6.QtGui import (
    QFont,
    QFontMetrics,
)

from app.core.log import get_logger

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget

_logger = get_logger(__name__)


class CenterUtils:
    @staticmethod
    def center(widget: QWidget, offset_x=0, offset_y=0):
        screen_rect = widget.screen().availableGeometry()
        widget_rect = widget.frameGeometry()
        center_point = screen_rect.center() + QPoint(offset_x, offset_y)
        widget_rect.moveCenter(center_point)
        widget.move(widget_rect.topLeft())


def read_stylesheet(style_sheets: list[str] = None) -> str:
    """
    Combine the content of multiple QSS files into one string.

    Args:
            style_sheets (list[str], optional): List of file paths to QSS files. Defaults to [].

    Returns:
            str: Combined content of all valid QSS files. If no valid file is found, an empty
            string is returned.
    """
    if style_sheets is None:
        style_sheets = []

    combined_styles = ""

    for path in style_sheets:
        try:
            with open(path) as f:
                combined_styles += f.read() + "\n"
        except FileNotFoundError:
            _logger.warning(f"QSS file not found: {path}. Skipping.")
        except PermissionError:
            _logger.error(f"No permission to read QSS file: {path}. Skipping.")
        except Exception as e:
            _logger.error(f"Error reading QSS file: {path}. Error: {e}. Skipping.")

    return combined_styles


def calculate_size_from_font(message: str, font: QFont):
    font_metrics = QFontMetrics(font)
    return font_metrics.boundingRect(message).size()
