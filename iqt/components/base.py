from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QApplication
from pydantic import BaseModel, Field

Size: tuple[int, int] = ...


class ConfigurableType(type):
    def __new__(cls, _name, bases, namespace, **opts):
        namespace["_cfg_extra"] = opts or {}
        return super().__new__(cls, _name, bases, namespace)


class SignalModel(BaseModel):
    type: Any = object
    name: str
    method: str


class BaseConfig(BaseModel, arbitrary_types_allowed=True):
    name: str = "object"
    text: str = ""
    margins: tuple[int, int, int, int] = Field(None)
    to_connect: dict[str, list] = Field({})
    signals: list[SignalModel] = Field([])
    size: Size = Field(None)
    fixed_size: Size = Field(None)
    fixed_width: int = Field(None)

    def get_settings(self):
        result = self.model_dump(by_alias=True, exclude_none=True)
        result["signals"] = self.signals
        return result


class BaseConfigResponse(BaseModel, arbitrary_types_allowed=True):
    to_connect: dict[str, list] = Field({})
    signals: list[SignalModel] = Field([])
    entity: Any
    widget_settings: dict
    widget: Any


class LayoutConfigResponse(BaseConfigResponse, arbitrary_types_allowed=True):
    layout_settings: dict
    layout: Any
    items: list


class BaseObject(metaclass=ConfigurableType):
    class Config(BaseConfig):
        ...

    name: str = "object"
    cfg: Config
    widget: QWidget
    factory: QWidget
    to_connect: dict = {}
    signals: list[SignalModel] = []

    _cfg_extra: dict = None

    def __init__(self, *args, **kwargs):
        self._cfg_extra = {**self._cfg_extra, **kwargs}

    def build_config(self):
        self.cfg = self.Config(**(self._cfg_extra or {}))
        return self.cfg

    def config(self):
        return BaseConfigResponse(
            to_connect=self.to_connect,
            signals=self.signals,
            entity=self,
            widget_settings=self.build_config().get_settings(),
            widget=self.factory,
        )

    def pre_init(self) -> None:
        ...

    def post_init(self) -> None:
        ...

    def init_widget(self, parent) -> None:
        return self.factory(parent)

    def create_widget(self, parent=None):
        self.pre_init()
        self.widget = self.init_widget(parent)
        self.post_init()
        return self.widget


class BaseWidget(BaseObject):
    factory: QObject
    items: Any
    window: Any

    def config(self):
        return LayoutConfigResponse(
            to_connect=self.to_connect,
            signals=self.signals,
            entity=self,
            widget_settings=self.build_config().get_settings(),
            layout_settings=self.items.build_config().get_settings(),
            widget=self.factory,
            layout=self.items.factory,
            items=self.items.items,
        )
