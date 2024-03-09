import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir

from iqt.components.base import BaseObject, BaseConfig
from iqt.utils import setup_fonts
from iqt.style import base_style
from iqt import logger
from typing import Any


class AppConfig(BaseConfig):
    style: str = base_style
    start_window: Any
    app_name: Any = "Base application"
    font_path: Path = Path().resolve() / "fonts"
    icon_path: Path = Path().resolve() / "icons"
    images_path: Path = Path().resolve() / "images"


class Application(BaseObject):
    main_window: Any
    Config = AppConfig

    def __init__(self):
        self.app = QApplication()

    def run(self):
        self.app.cfg = self.cfg = self.build_config()
        self.pre_init()

        logger.debug(f"{self.cfg.app_name} starting...")

        QDir.addSearchPath('images', str(self.cfg.images_path))
        QDir.addSearchPath('icons', str(self.cfg.icon_path))
        setup_fonts(self.app)

        window: Any = self.cfg.start_window(self)
        window.init_window()

        self.post_init()
        self.app.setStyleSheet(self.cfg.style)
        sys.exit(self.app.exec())
