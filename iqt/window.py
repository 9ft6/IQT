from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QEvent, QPropertyAnimation, QEasingCurve, QPoint

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.components import Widget
from iqt.components.layouts import Horizont, HorizontNM
from iqt.components.title_bar import TitleBar
from iqt.utils import setup_settings, get_widget_center_geometry


class CentralWidget(Widget, name="central_widget"):
    items = HorizontNM[None]

    def set_widget(self, widget: BaseObject, transparent: bool):
        self.widget.clear()
        self.widget.add_widget(widget)

        if transparent:
            TitleBar().create_widget(widget)


class MainWindow(QMainWindow):
    size_value: tuple[int, int]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.central_widget = CentralWidget().create_widget(self)
        self.setCentralWidget(self.central_widget)

    def eventFilter(self, obj, event):
        click_init_events = [
            QEvent.MouseButtonDblClick,
            QEvent.MouseButtonPress,
        ]
        if event.type() in click_init_events:
            if event.y() < 32:
                self.old_pos = event.globalPos()
            else:
                self.old_pos = 0
        elif event.type() == QEvent.MouseMove and self.entity.cfg.transparent:
            if getattr(self, 'old_pos', None):
                self.do_move_action(event)
                self.old_pos = event.globalPos()

        return QMainWindow.eventFilter(self, obj, event)

    def do_move_action(self, event):
        if self.isMaximized():
            return

        try:
            delta = QPoint(event.globalPos() - self.old_pos)
        except:
            return
        self.move(self.x() + delta.x(), self.y() + delta.y())

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

    def move_to_center(self, size, animation=True):
        final = get_widget_center_geometry(size)
        if animation:
            self.start_resize_animation(final)
        else:
            self.setGeometry(final)

    def change_widget(self, widget: Widget, animation=True):
        if not isinstance(widget, Widget):
            class Wrapper(Widget):
                items = Horizont[widget]

            widget = Wrapper()

        widget = widget.create_widget(self)
        widget.window = widget.entity.window = self
        self.current = widget
        self.central_widget.entity.set_widget(widget, self.entity.cfg.transparent)

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

        if self.cfg.transparent:
            self.window.setWindowFlags(Qt.FramelessWindowHint)
            self.window.setAttribute(Qt.WA_TranslucentBackground, True)
            self.window.central_widget.setProperty("transparent", False)

        setup_settings(self.window, self.cfg.get_settings())
        self.window.setup_animation()
        self.widget = self.set_widget(self.cfg.widget_model(), animation=False)

        if self.cfg.start_at_center and self.cfg.size:
            self.window.resize(*self.cfg.size)
            self.window.move_to_center(self.cfg.size, animation=False)

        self.window.show()
        self.post_init()

    def set_widget(self, widget, animation=True):
        self.window.change_widget(widget, animation=animation)
        return widget
