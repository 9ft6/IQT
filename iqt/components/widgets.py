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
        widget = layout.init_widget()
        self.connect_signals(layout.items)
        return widget

    def connect_signals(self, items):
        for item in items:
            if item is Ellipsis or not item.cfg.signals:
                continue

            for method_name, signals in item.cfg.signals.items():
                for signal_name in signals:
                    self.connect_signal(item, signal_name, method_name)

    def connect_signal(self, item, signal_name, method_name):
        if signal := getattr(item.widget, signal_name, None):
            if method := getattr(self, method_name, None):
                signal.connect(method)

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


class BaseCheckBox(
    TextArgumentMixin,
    BaseWidgetObject,
    name="default_checkbox"
):
    factory: QWidget = QCheckBox