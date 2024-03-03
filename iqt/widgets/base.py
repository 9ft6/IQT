from abc import abstractmethod
from typing import Any

from PySide6.QtWidgets import QWidget, QBoxLayout
from pydantic import BaseModel, Field

from iqt.utils import setup_settings

Size: tuple[int, int] = ...


class ConfigurableType(type):
    def __new__(cls, _name, bases, namespace, **opts):
        namespace["_cfg_extra"] = opts or {}
        return super().__new__(cls, _name, bases, namespace)


class BaseConfig(BaseModel, arbitrary_types_allowed=True):
    factory: Any = None
    init_args: tuple = Field(default_factory=tuple)
    init_kwargs: dict = Field(default_factory=dict)

    # settings
    name: str = "default_object"
    size: Size = None
    fixed_size: Size = None

    def get_settings(self):
        result = self.model_dump(exclude={
            "factory",
            "widget_model",
            "layout",
            "init_args",
            "init_kwargs",
        }, by_alias=True, exclude_none=True)

        return result


class BaseObject(metaclass=ConfigurableType):
    class Config(BaseConfig):
        ...

    cfg: Config
    widget: QWidget

    _cfg_extra: dict = None

    @abstractmethod
    def build_config(self):
        return self.Config(**(self._cfg_extra or {}))

    def factory(self):
        return self.cfg.factory(*self.cfg.init_args, **self.cfg.init_kwargs)

    @abstractmethod
    def pre_init(self) -> None:
        ...

    @abstractmethod
    def post_init(self) -> None:
        ...


class BaseWidgetObject(BaseObject):
    def init_widget(self) -> QWidget:
        self.pre_init()
        self.cfg = self.build_config()
        self.name = self.cfg.name
        self.widget = self.factory()
        setup_settings(self.widget, self.cfg)
        self.post_init()
        return self.widget
