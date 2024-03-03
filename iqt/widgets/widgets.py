from abc import abstractmethod

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QCheckBox

from iqt.widgets.base import BaseConfig, BaseWidgetObject
from iqt.widgets.layouts import BaseLayout

Size: tuple[int, int] = ...


class WidgetConfig(BaseConfig):
    layout: BaseLayout


class Widget(BaseWidgetObject):
    class Config(WidgetConfig):
        name: str

    cfg: WidgetConfig

    def factory(self):
        return self.cfg.layout.init_widget()

    @abstractmethod
    def items_handler(self, *args, **kwargs):
        ...


class BaseLabel(BaseWidgetObject):
    class Config(BaseConfig):
        name: str = "default_label"
        factory: QWidget = QLabel

    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg


class BaseInput(BaseWidgetObject):
    class Config(BaseConfig):
        name: str = "default_input"
        factory: QWidget = QLineEdit

    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg


class BaseButton(BaseWidgetObject):
    class Config(BaseConfig):
        name: str = "default_button"
        factory: QWidget = QPushButton

    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg


class BaseCheckBox(BaseWidgetObject):
    class Config(BaseConfig):
        name: str = "default_checkbox"
        factory: QWidget = QCheckBox

    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg
