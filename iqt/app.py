import sys
from pathlib import Path
from typing import Any

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir

from iqt.components.base import BaseObject, BaseConfig
from iqt.utils import setup_fonts
from iqt.style import base_style
from iqt import logger


class AppConfig(BaseConfig):
    style: str = base_style
    app_name: Any = "Base application"
    font_path: Path = Path().resolve() / "fonts"
    icon_path: Path = Path().resolve() / "icons"
    images_path: Path = Path().resolve() / "images"


class Application(BaseObject):
    main_window: Any
    StartWindow: Any
    Config = AppConfig

    def run(self):
        self.app = QApplication()
        self.app.cfg = self.cfg = self.build_config()
        self.app.setStyleSheet(self.cfg.style)
        self.pre_init()

        logger.debug(f"{self.cfg.app_name} starting...")

        QDir.addSearchPath('images', str(self.cfg.images_path))
        QDir.addSearchPath('icons', str(self.cfg.icon_path))
        setup_fonts(self.app)

        window: Any = self.StartWindow(self)
        window.init_window()

        self.post_init()
        sys.exit(self.app.exec())
