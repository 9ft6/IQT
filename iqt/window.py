from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QRect

from iqt.widgets.base import Size, BaseObject, BaseConfig
from iqt.utils import setup_settings


class WindowConfig(BaseConfig):
    widget_model: BaseObject = None
    title: str = "Application"
    fixed_size: Size = None
    transparent: bool = False
    name: str = "default_window"
    start_at_center: bool = True


class Window(QMainWindow):
    class Config(WindowConfig):
        ...

    cfg: WindowConfig = Config()

    def __init__(self, app: QApplication):
        self.app = app

        super(Window, self).__init__()
        self.cfg = self.Config()

        setup_settings(self, self.cfg)
        self.setAttribute(Qt.WA_TranslucentBackground, self.cfg.transparent)
        widget = self.cfg.widget_model().init_widget()
        self.setCentralWidget(widget)

        if self.cfg.start_at_center:
            self.move_to_center()

        self.show()

    def move_to_center(self):
        center = QApplication.primaryScreen().geometry().center()
        x, y, (w, h) = center.x(), center.y(), self.size().toTuple()
        self.setGeometry(QRect(x - w / 2, y - h / 2, w, h))
