from typing import Literal

from PySide6.QtWidgets import QWidget, QScrollArea

from iqt.components.base import Size, BaseObject, BaseConfig
from iqt.components.widgets import Widget, BaseWidget
from iqt.components.layouts import Horizont
from iqt.utils import setup_settings


class DataViewWidget(QScrollArea):
    ...


class DataView(BaseObject):
    class Config(BaseConfig):
        name: str = "data_view"
        direction: Literal["vertical", "horizont", "flow"] = "vertical"

    items: dict
    factory: QWidget = DataViewWidget

    def __init__(self, name=None, *args, **kwargs):
        kwargs["name"] = name
        super().__init__(*args, **kwargs)

    def add(self, widget: BaseObject | list[BaseObject]):
        print(widget)

    def remove(self, num: int):
        ...

    def clear(self):
        ...

    def post_init(self) -> None:
        copy_methods = ["add", "remove", "clear"]
        [setattr(self.widget, m, v) for m in copy_methods
         if (v := getattr(self, m, None))]
