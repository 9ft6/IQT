from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QRect

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.utils import setup_settings


class WindowConfig(BaseConfig):
    widget_model: Any = None
    title: str = "Application"
    fixed_size: Size = None
    transparent: bool = False
    name: str = "default_window"
    start_at_center: bool = True


class Window(BaseObject):
    window: QMainWindow
    Config = WindowConfig

    def __init__(self, app: QApplication):
        self.app = app

    def init_window(self):
        self.pre_init()

        self.window = QMainWindow()
        self.window.entity = self
        self.cfg = self.build_config()

        setup_settings(self.window, self.cfg)
        self.window.setAttribute(Qt.WA_TranslucentBackground, self.cfg.transparent)
        self.widget = widget = self.cfg.widget_model().init_widget()
        self.window.setCentralWidget(widget)

        if self.cfg.start_at_center:
            self.move_to_center()

        self.post_init()
        self.window.show()

    def move_to_center(self):
        center = QApplication.primaryScreen().geometry().center()
        x, y, (w, h) = center.x(), center.y(),  self.window.size().toTuple()
        self.window.setGeometry(QRect(x - w / 2, y - h / 2, w, h))
