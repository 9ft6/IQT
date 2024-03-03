from iqt.components.base import BaseConfig, BaseWidgetObject
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout


class BaseLayoutConfig(BaseConfig):
    spacing: int = 4


class BaseLayout(BaseWidgetObject):
    items: tuple

    def __init__(self, items):
        self.items = items

    @classmethod
    def __class_getitem__(cls, key):
        return cls(key if isinstance(key, tuple) else (key, ))

    def create_widget(self) -> QWidget:
        widget = QWidget(*self.cfg.init_args, **self.cfg.init_kwargs)
        layout = self.factory(widget)
        for item in self.items:
            if item is Ellipsis:
                layout.addStretch()
            else:
                layout.addWidget(item.init_widget())

        return widget


class BaseHorizont(BaseLayout, name="base_horizont"):
    factory: QBoxLayout = QHBoxLayout


class BaseVertical(BaseLayout, name="base_vertical"):
    factory: QBoxLayout = QVBoxLayout