from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QRect

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.components import Widget
from iqt.components.layouts import Horizont
from iqt.utils import setup_settings


class MainWindow(QMainWindow):
    def move_to_center(self):
        center = QApplication.primaryScreen().geometry().center()
        x, y, (w, h) = center.x(), center.y(), self.size().toTuple()
        self.setGeometry(QRect(x - w / 2, y - h / 2, w, h))

    def change_widget(self, widget: Widget):
        if isinstance(widget, Widget):
            widget = widget.widget()
        else:
            class Wrapper(Widget):
                items = Horizont[widget]

            widget = Wrapper().widget()

        widget.window = widget.entity.window = self
        self.setCentralWidget(widget)
        self.setFixedSize(widget.size())
        self.move_to_center()
        print()


class WindowConfig(BaseConfig):
    widget_model: Any = None
    title: str = "Application"
    fixed_size: Size = None
    transparent: bool = False
    name: str = "window"
    start_at_center: bool = True


class Window(BaseObject):
    factory: QMainWindow = MainWindow
    window: MainWindow
    Config = WindowConfig

    def __init__(self, app: QApplication):
        self.app = app

    def init_window(self):
        self.window = self.factory()
        self.window.entity = self
        self.cfg = self.build_config()
        self.pre_init()

        setup_settings(self.window, self.cfg.get_settings())
        self.window.setAttribute(Qt.WA_TranslucentBackground, self.cfg.transparent)

        self.widget = self.set_widget(self.cfg.widget_model())

        if self.cfg.start_at_center:
            self.window.move_to_center()

        self.window.show()
        self.post_init()

    def set_widget(self, widget):
        self.window.change_widget(widget)
        return widget

    def pre_init(self) -> None:
        ...

    def post_init(self) -> None:
        ...
