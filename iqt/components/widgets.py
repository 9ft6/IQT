from PySide6.QtWidgets import QPushButton, QLineEdit, QCheckBox, QWidget

from iqt.components.base import BaseConfig, BaseWidgetObject
from iqt.components.layouts import BaseLayout

Size: tuple[int, int] = ...


class WidgetConfig(BaseConfig):
    layout: BaseLayout = None


class Widget(BaseWidgetObject):
    Config = WidgetConfig

    def post_init(self):
        self.widget.entity = self
        self.widget.add_widget = self.add_widget

    def factory(self):
        layout = self.cfg.layout or self.generate_layout()
        return layout.init_widget()

    def generate_layout(self):
        ...

    def items_handler(self, *args, **kwargs):
        ...

    def add_widget(self, widget):
        self.widget.layout().addWidget(widget.init_widget())


class TextArgumentMixin:
    def __init__(self, text=None, **kwargs):
        self.text = text

    def build_config(self):
        cfg = super().build_config()
        cfg.init_args = (self.text, )
        return cfg


class BaseInput(
    TextArgumentMixin,
    BaseWidgetObject,
    name="default_input"
):
    factory: QWidget = QLineEdit


class BaseButton(
    TextArgumentMixin,
    BaseWidgetObject,
    name="default_button"
):
    factory: QWidget = QPushButton


class BaseCheckBox(
    TextArgumentMixin,
    BaseWidgetObject,
    name="default_checkbox"
):
    factory: QWidget = QCheckBox