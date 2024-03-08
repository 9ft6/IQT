from types import MethodType
from typing import Any

from PySide6.QtWidgets import QWidget, QCheckBox, QLineEdit, QLabel
from PySide6.QtCore import Signal, QObject

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
    root: Any
    entity: Any

    __signals: QObject

    def build(self, config, root=None):
        self.root = root or self
        self.entity = config.entity

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

        self.create_signals(self, config)
        self.entity.widget = self
        return self

    def make_items(self, item, parent=None):
        from iqt.components.layouts import BaseLayout, BaseObject

        config = item.config()
        widget = config.widget(parent)
        match item:
            case BaseLayout() | BaseWidget():
                widget.build(config, root=parent.root)
            case BaseObject():
                setup_settings(widget, config.widget_settings)
                setattr(self, widget.name, widget)
                self.create_signals(widget, item)

        return widget

    def create_signals(self, widget, settings):
        if signals := settings.signals:
            class_attrs = {s.name: Signal(s.type) for s in signals}
            self.__signals = type('Signals', (QObject,), class_attrs)()
            for signal in signals:
                obj = getattr(self.__signals, signal.name)
                setattr(self, signal.name, obj)

        self.connect_signals(widget, settings.to_connect)

    def connect_signals(self, widget, signals):
        match signals:
            case dict():
                for method_name, signals in signals.items():
                    self.connect_signals(widget, [(method_name, s) for s in signals])
            case list():
                [self.connect_signals(widget, s) for s in signals]
            case tuple():
                method_name, signal_name = signals
                if method := self.find_method(method_name):
                    if signal := get_attr_recursive(widget, signal_name):
                        if isinstance(method.__self__, QObject) or widget is self:
                            signal.connect(method)
                        else:
                            setattr(widget, method_name, MethodType(method, widget))
                            method = getattr(widget, method_name)

                        signal.connect(method)

    def find_method(self, method_name):
        if "." in method_name:
            parent_name, method_name = method_name.split(".", 1)
            if parent := get_attr_recursive(self, parent_name):
                return parent.find_method(method_name)
        else:
            return self.get_grand_pa(self, method_name)

    def get_grand_pa(self, widget, method_name):
        parent = widget
        while parent:
            if result := getattr(parent, method_name, None):
                return result

            if isinstance(parent, CustomQWidget):
                result = getattr(parent.entity, method_name, None)

            if result:
                return result

            parent = parent.parent()


class Widget(BaseWidget):
    factory: QWidget = CustomQWidget
    to_connect: dict[str, list[str]] = {}
    signals: list = []

    def widget(self):
        return self.factory().build(self.config())
