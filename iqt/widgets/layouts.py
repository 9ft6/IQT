from iqt.widgets.base import BaseObject, BaseConfig
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


class BaseLayoutConfig(BaseConfig):
    ...


class BaseLayout(BaseObject):
    items: tuple

    def __init__(self, items):
        self.items = items

    @classmethod
    def __class_getitem__(cls, key):
        return cls(key if isinstance(key, tuple) else (key, ))

    def factory(self) -> QWidget:
        widget = QWidget(*self.cfg.init_args, **self.cfg.init_kwargs)
        layout = self.cfg.factory(widget)
        for item in self.items:
            if item is Ellipsis:
                layout.addStretch()
            else:
                layout.addWidget(item.init_widget())

        return widget


class BaseHorizont(BaseLayout):
    class Config(BaseLayoutConfig):
        factory: QWidget = QHBoxLayout
        name: str = "base_horizont"


class BaseVertical(BaseLayout):
    class Config(BaseLayoutConfig):
        factory: QWidget = QVBoxLayout
        name: str = "base_vertical"
