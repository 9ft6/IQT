import sys
from pathlib import Path

from pydantic import BaseModel
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir

from iqt.utils import setup_fonts
from iqt.style import base_style
from iqt import logger
from typing import Any


class AppConfig(BaseModel, arbitrary_types_allowed=True):
    style: str = base_style
    window_model: Any
    app_name: Any = "Base application"
    font_path: Path = Path().resolve() / "fonts"
    icon_path: Path = Path().resolve() / "icons"
    images_path: Path = Path().resolve() / "images"


class Application(QApplication):
    class Config(AppConfig):
        ...

    cfg: Config
    main_window: Any

    def __init__(self):
        self.cfg = self.Config()
        logger.debug(f"{self.cfg.app_name} starting...")
        super(Application, self).__init__()
        QDir.addSearchPath('images', str(self.cfg.images_path))
        QDir.addSearchPath('icons', str(self.cfg.icon_path))
        setup_fonts(self)

        self.setStyleSheet(self.cfg.style)
        self.main_window: Any = self.cfg.window_model(self)

        sys.exit(self.exec())
