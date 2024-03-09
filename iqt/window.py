from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QRect, Property, QPropertyAnimation, QEasingCurve

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.components import Widget
from iqt.components.layouts import Horizont
from iqt.utils import setup_settings


class MainWindow(QMainWindow):
    size_value: tuple[int, int]

    def setup_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setDuration(100)

    def start_resize_animation(self, final_rect):
        initial_rect = self.geometry()
        final_rect.moveCenter(initial_rect.center())
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(final_rect)
        self.anim.start()

    def move_to_center(self, fixed_size, animation=True):
        center = QApplication.primaryScreen().geometry().center()
        x, y, (w, h) = center.x(), center.y(), self.size().toTuple()
        final = QRect(x - w / 2, y - h / 2, *fixed_size)
        if animation:
            self.start_resize_animation(final)
        else:
            self.setGeometry(final)

    def change_widget(self, widget: Widget, animation=True):
        if isinstance(widget, Widget):
            widget = widget.widget()
        else:
            class Wrapper(Widget):
                items = Horizont[widget]

            widget = Wrapper().widget()

        widget.window = widget.entity.window = self
        self.setCentralWidget(widget)

        fixed_size = self.entity.cfg.fixed_size or widget.size().toTuple()
        self.move_to_center(fixed_size, animation=animation)


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
        self.window.setup_animation()
        self.widget = self.set_widget(self.cfg.widget_model(), animation=False)

        widget_size = self.widget.widget.size().toTuple()
        if self.cfg.start_at_center:
            self.window.move_to_center(widget_size, animation=False)

        self.window.show()
        self.post_init()

    def set_widget(self, widget, animation=True):
        self.window.change_widget(widget, animation=animation)
        return widget

    def pre_init(self) -> None:
        ...

    def post_init(self) -> None:
        ...
