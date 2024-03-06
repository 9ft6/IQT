from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
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


class BaseObject(metaclass=ConfigurableType):
    class Config(BaseConfig):
        ...

    name: str = "object"
    cfg: Config
    widget: QWidget
    widget_model: Any

    _cfg_extra: dict = None

    def __init__(self, *args, **kwargs):
        self._cfg_extra = {**self._cfg_extra, **kwargs}

    def build_config(self):
        self.cfg = self.Config(**(self._cfg_extra or {}))
        return self.cfg


class BaseWidget(BaseObject):
    factory: QObject
    to_connect: QObject = []

    def get_items(self):
        self.build_config()
        return {
            "to_connect": self.to_connect,
            "entity": self,
            "settings": self.cfg.get_settings(),
            "factory": self.factory
        }
