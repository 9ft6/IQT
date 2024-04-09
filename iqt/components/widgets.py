from types import MethodType
from typing import Any

from PySide6.QtWidgets import QWidget, QCheckBox, QLineEdit, QApplication
from PySide6.QtCore import Signal, QObject, Qt

from iqt.components.base import BaseWidget, BaseObject, BaseConfig
from iqt.utils import (
    setup_settings,
    get_attr_recursive,
    get_widget_center_geometry,
)

Size: tuple[int, int] = ...


class Input(BaseObject):
    class Config(BaseConfig):
        fixed_height: int = 24

    factory: QWidget = QLineEdit
    to_connect: dict = {
        "text_handler": ["textChanged"],
        "items_handler": ["editingFinished"],
    }

    def __init__(self, name=None, *args, **kwargs):
        kwargs["name"] = name
        super().__init__(*args, **kwargs)


class CustomQWidget(QWidget):
    root: Any
    entity: Any

    __signals: QObject

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hide = super().hide
        self._show = super().show

    def build(self, config, root=None):
        self.root = root or self
        self.entity = config.entity
        self.setAttribute(Qt.WA_StyledBackground)
        self.app = QApplication.instance()

        layout = config.layout(self)

        setup_settings(layout, config.layout_settings)
        setup_settings(self, config.widget_settings)

        for item in (self.entity.generate_items() or config).items:
            if not item:
                continue

            if item is Ellipsis:
                layout.addStretch()
            else:
                widget = self.add_widget_to_layout(item, layout=layout)
                self.set_widget_attr(widget.name, widget)

        self.create_signals(self, config)
        self.entity.widget = self
        return self

    def move_to_center(self, size=None, animation=True):
        size = size or self.size().toTuple()
        self.setGeometry(get_widget_center_geometry(size))

    def add_widget_to_layout(self, widget, layout=None):
        layout = layout or self.layout()
        if not isinstance(widget, QWidget):
            widget = self.make_items(widget, parent=self)
        layout.addWidget(widget)
        return widget

    def add_widget(self, widget):
        return self.add_widget_to_layout(widget)

    def clear(self):
        while item := self.layout().itemAt(0):
            if widget := item.widget():
                widget.hide()
                self.layout().removeWidget(widget)
            else:
                self.layout().removeItem(item.spacerItem())

    def set_widget_attr(self, name, widget):
        objects = [self, self.entity, self.root, self.root.entity]
        [setattr(o, name, widget) for o in objects]

    def make_items(self, item, parent=None):
        from iqt.components.layouts import BaseLayout, BaseObject

        config = item.config()
        match item:
            case BaseWidget():
                widget = config.entity.create_widget(parent)
            case BaseLayout():
                widget = config.widget(parent)
                widget.build(config, root=parent.root)
            case BaseObject():
                widget = config.entity.create_widget(parent)
                self.set_widget_attr(widget.name, widget)
                self.create_signals(widget, item)

        return widget

    def create_signals(self, widget, settings):
        if signals := settings.signals:
            class_attrs = {s.name: Signal(s.type) for s in signals}
            self.__signals = type('Signals', (QObject,), class_attrs)()
            for signal in signals:
                obj = getattr(self.__signals, signal.name)
                self.set_widget_attr(signal.name, obj)

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
                    if signal := get_attr_recursive(widget, signal_name, with_parent=widget is self):
                        if isinstance(method.__self__, QObject):
                            signal.connect(method)
                        elif widget is self:
                            signal, parent = signal
                            setattr(parent, method_name, MethodType(method, parent))
                            method = getattr(parent, method_name)
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

    def __init__(self, name=None, *args, **kwargs):
        if name:
            kwargs["name"] = name
        super().__init__(*args, **kwargs)

    def generate_items(self):
        ...

    def init_widget(self, parent=None):
        return self.factory(parent).build(self.config())
