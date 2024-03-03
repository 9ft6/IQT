from abc import abstractmethod

from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QCheckBox

from iqt.widgets.base import BaseConfig, BaseWidgetObject
from iqt.widgets.layouts import BaseLayout

Size: tuple[int, int] = ...


class WidgetConfig(BaseConfig):
    layout: BaseLayout


class Widget(BaseWidgetObject):
    Config = WidgetConfig

    def factory(self):
        return self.cfg.layout.init_widget()

    @abstractmethod
    def items_handler(self, *args, **kwargs):
        ...


class TextArgumentMixin:
    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg


class BaseLabel(
    TextArgumentMixin,
    BaseWidgetObject,
    factory=QLabel,
    name="default_label"
):
    ...


class BaseInput(
    TextArgumentMixin,
    BaseWidgetObject,
    factory=QLineEdit,
    name="default_input"
):
    ...


class BaseButton(
    TextArgumentMixin,
    BaseWidgetObject,
    factory=QPushButton,
    name="default_button"
):
    ...


class BaseCheckBox(
    TextArgumentMixin,
    BaseWidgetObject,
    factory=QCheckBox,
    name="default_checkbox"
):
    ...