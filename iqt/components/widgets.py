from types import MethodType

from PySide6.QtWidgets import QLineEdit, QCheckBox, QWidget

from iqt.components.base import BaseConfig, BaseWidgetObject
from iqt.components.layouts import BaseLayout

Size: tuple[int, int] = ...


class WidgetConfig(BaseConfig):
    layout: BaseLayout = None


class Widget(BaseWidgetObject):
    Config = WidgetConfig

    def post_init(self):
        self.widget.entity = self

    def create_widget(self, parent=None):
        layout = self.cfg.layout or self.generate_layout()
        return self.create_items(layout.get_construct(), root=self)

    def create_items(self, items, root=None):
        match items:
            case dict():
                widget = QWidget()
                layout = items["entity"].factory(widget)
                for item in items["items"]:
                    if item is Ellipsis:
                        layout.addStretch()
                    else:
                        layout.addWidget(self.create_items(item, root=root))
                return widget
            case _:
                widget = items.init_widget()
                if root and items.cfg.signals:
                    self.connect_signals(root, items)
                return widget

    def connect_signals(self, root, item):
        for method_name, signals in item.cfg.signals.items():
            for signal in signals:
                self.connect_signal(item, signal, root, method_name)

    def connect_signal(self, item, signal_name, root, method_name):
        if signal := getattr(item.widget, signal_name, None):
            if method := getattr(root, method_name, None):
                setattr(item.widget, method_name, MethodType(method, item.widget))
                signal.connect(getattr(item.widget, method_name, None))

    def generate_layout(self):
        ...

    def items_handler(self, *args, **kwargs):
        ...

    def add_widget(self, widget):
        ...


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
    name="input"
):
    factory: QWidget = QLineEdit


class BaseCheckBox(
    TextArgumentMixin,
    BaseWidgetObject,
    name="checkbox"
):
    factory: QWidget = QCheckBox