from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.components import Widget
from iqt.components.layouts import Horizont
from iqt.utils import setup_settings


class MainWindow(QMainWindow):
    size_value: tuple[int, int]

    def setup_animation(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.setDuration(120)

    def start_resize_animation(self, final_rect):
        initial_rect = self.geometry()
        final_rect.moveCenter(initial_rect.center())
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(final_rect)
        self.anim.start()

    def move_to_center(self, fixed_size, animation=True):
        screen = QApplication.primaryScreen().geometry().center()
        center = screen
        x, y, (w, h) = center.x(), center.y(), fixed_size
        final = QRect(x - w / 2, y - h/2, *fixed_size)
        if animation:
            self.start_resize_animation(final)
        else:
            self.setGeometry(final)

    def change_widget(self, widget: Widget, animation=True):
        if isinstance(widget, Widget):
            widget = widget.create_widget(self)
        else:
            class Wrapper(Widget):
                items = Horizont[widget]

            widget = Wrapper().create_widget(self)

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
        self.window.setVisible(False)
        self.window.entity = self
        self.cfg = self.build_config()

        self.pre_init()

        setup_settings(self.window, self.cfg.get_settings())
        self.window.setAttribute(Qt.WA_TranslucentBackground, self.cfg.transparent)
        self.window.setup_animation()
        widget = self.cfg.widget_model()
        self.widget = self.set_widget(widget, animation=False)

        if self.cfg.start_at_center and self.cfg.size:
            self.window.resize(*self.cfg.size)
            self.window.move_to_center(self.cfg.size, animation=False)
        self.window.setVisible(True)
        self.window.show()
        self.post_init()

    def set_widget(self, widget, animation=True):
        self.window.change_widget(widget, animation=animation)
        return widget
