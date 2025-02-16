from __future__ import annotations

import sys
import argparse
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.core.log import setup_logging
from app.ui import create_window


setup_logging(log_level="DEBUG")


def main(
    app_version: str,
    app_name: str = "Live Chart",
    editor_html: Path | str = None,
) -> None:
    app = QApplication(sys.argv)

    create_window(app_version=app_version, app_name=app_name)

    from app.ui import context
    from app.ui.pages.workspace import WorkspaceUI

    context.switch_ui(WorkspaceUI, editor_html)

    context.show_ui()

    sys.exit(app.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Live Chart")
    parser.add_argument(
        "--version", type=str, default="1.0.0", help="Application version"
    )
    parser.add_argument(
        "--name", type=str, default="Live Chart", help="Application name"
    )
    parser.add_argument("--editor", type=str, help="Path to editor HTML file")
    args = parser.parse_args()

    if args.editor is None:
        args.editor = Path(__file__).parent.parent / "static" / "html" / "editor.html"

    main(
        app_version=args.version,
        app_name=args.name,
        editor_html=args.editor,
    )
