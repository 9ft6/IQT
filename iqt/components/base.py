from typing import Any

from PySide6.QtWidgets import QWidget
from pydantic import BaseModel, Field

from iqt.utils import setup_settings

Size: tuple[int, int] = ...


class ConfigurableType(type):
    def __new__(cls, _name, bases, namespace, **opts):
        namespace["_cfg_extra"] = opts or {}
        return super().__new__(cls, _name, bases, namespace)


class BaseConfig(BaseModel, arbitrary_types_allowed=True):
    init_args: tuple = Field(default_factory=tuple)
    init_kwargs: dict = Field(default_factory=dict)

    # settings
    name: str = "default_object"
    margins: tuple[int, int, int, int] = Field(None)
    signals: dict[str, list] = Field(None)
    size: Size = Field(None)
    fixed_size: Size = Field(None)
    fixed_width: int = Field(None)

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

    name: str = "default_object"
    cfg: Config
    widget: QWidget
    factory: Any

    _cfg_extra: dict = None

    def build_config(self):
        return self.Config(**(self._cfg_extra or {}))

    def create_widget(self):
        return self.factory(*self.cfg.init_args, **self.cfg.init_kwargs)

    def pre_init(self) -> None:
        ...

    def post_init(self) -> None:
        ...


class BaseWidgetObject(BaseObject):
    def init_widget(self) -> QWidget:
        self.cfg = self.build_config()
        self.pre_init()

        self.cfg.name = self.name or self.cfg.name
        self.widget = self.create_widget()
        self.widget.entity = self
        setattr(self, self.name, self.widget)
        setup_settings(self.widget, self.cfg)

        self.post_init()
        return self.widget
