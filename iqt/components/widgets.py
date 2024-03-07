from types import MethodType
from typing import Any

from PySide6.QtWidgets import QWidget, QCheckBox, QLineEdit, QLabel
from PySide6.QtCore import Signal

from iqt.components.base import BaseWidget, BaseObject
from iqt.utils import setup_settings, get_attr_recursive

Size: tuple[int, int] = ...


class Input(BaseObject):
    factory: QWidget = QLineEdit

    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = text
        super().__init__(*args, **kwargs)


class CheckBox(BaseObject):
    factory: QWidget = QCheckBox


class CustomQWidget(QWidget):
    _entity: Any

    def build(self, config, root=None):
        self._entity = root or config.entity
        layout = config.layout(self)

        setup_settings(layout, config.layout_settings)
        setup_settings(self, config.widget_settings)

        for item in config.items:
            if item is Ellipsis:
                layout.addStretch()
            else:
                widget = self.make_items(item, parent=self)
                setattr(self, widget.name, widget)
                layout.addWidget(widget)

        return self

    def make_items(self, item, parent=None):
        from iqt.components.layouts import BaseLayout

        match item:
            case list():
                return [self.make_items(i, parent=parent) for i in item]
            case type(Ellipsis()):
                return item
            case BaseLayout() | BaseWidget():
                config = item.config()
                widget = config.widget(parent=parent)
                widget.build(config, root=self._entity)
                return widget
            case _:
                config = item.config()
                widget = config.widget(parent)
                setup_settings(widget, config.widget_settings)
                setattr(self, widget.name, widget)
                self.create_signals(widget, item)
                return widget

    def create_signals(self, widget, settings):
        if signals := settings.signals:
            for signal in signals:
                setattr(self, signal.name, Signal(signal.type))
                self.connect_signals(widget, (signal.method, signal.name))

        if signals := settings.to_connect:
            self.connect_signals(widget, signals)

    def connect_signals(self, widget, signals):
        match signals:
            case dict():
                for method_name, signals in signals.items():
                    self.connect_signals(widget, [(method_name, s) for s in signals])
            case list():
                [self.connect_signals(widget, s) for s in signals]
            case tuple():
                method_name, signal_name = signals
                if method := self.ensure_method(widget, method_name):
                    if signal := get_attr_recursive(widget, signal_name):
                        print(f'   connect {signal_name} --> {method_name}')
                        signal.connect(method)

    def ensure_method(self, widget, method_name):
        if low_method := get_attr_recursive(self, method_name):
            return low_method
        else:
            if high_method := get_attr_recursive(self._entity, method_name):
                setattr(widget, method_name, MethodType(high_method, widget))
                return get_attr_recursive(widget, method_name)


class Widget(BaseWidget):
    factory: QWidget = CustomQWidget
    to_connect: dict[str, list[str]] = {}
    signals: list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def widget(self):
        return self.factory().build(self.config())
