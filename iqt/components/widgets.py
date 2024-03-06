from types import MethodType

from PySide6.QtWidgets import QWidget, QCheckBox, QLineEdit
from PySide6.QtCore import Signal

from iqt.components.base import BaseWidget
from iqt.components.layouts import BaseLayout
from iqt.utils import setup_settings, get_attr_recursive

Size: tuple[int, int] = ...


class Input(BaseWidget):
    factory: QWidget = QLineEdit

    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = text
        super().__init__(*args, **kwargs)


class CheckBox(BaseWidget):
    factory: QWidget = QCheckBox


class CustomQWidget(QWidget):
    _items: dict

    def __init__(self, items, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._items = items
        self._entity = items["entity"]
        self.make_items(items, is_root=True)

    def make_items(self, items, parent=None, is_root=False):
        if widgets := items.get("items"):
            widget = self if is_root else QWidget(parent)
            layout = items["layout"](widget)

            setup_settings(widget, items["widget_settings"])
            setup_settings(layout, items["layout_settings"])
            if name := getattr(widget, "name", None):
                setattr(self, name, widget)

            for item in widgets:
                if isinstance(item, type(Ellipsis)):
                    layout.addStretch()
                else:
                    layout.addWidget(self.make_items(item, parent=parent))

            self.create_signals(widget, items)
            return widget
        else:
            widget = items["factory"](parent)
            setup_settings(widget, items["settings"])
            setattr(self, widget.name, widget)
            self.create_signals(widget, items)
            return widget

    def create_signals(self, widget, settings):
        if signals := settings.get("signals"):
            for signal in signals:
                setattr(self, signal.name, Signal(signal.type))
                self.connect_signals(widget, (signal.method, signal.name))

        if signals := settings.get("to_connect"):
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
    items: BaseLayout
    to_connect: dict[str, list[str]] = {}
    signals: list = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_items(self):
        self.build_config()
        return {
            "to_connect": self.to_connect,
            "signals": self.signals,
            "entity": self,
            "widget_settings": self.cfg.get_settings(),
            "layout_settings": {},
            "factory": self.factory,
            "layout": self.items.factory,
            "items": [
                i if isinstance(i, type(Ellipsis)) else i.get_items()
                for i in self.items.items
            ],
        }

    def widget(self):
        self.build_config()
        return self.factory(self.get_items())
