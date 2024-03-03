from PySide6.QtWidgets import QWidget
from pydantic import BaseModel, Field

from iqt.utils import setup_settings

Size: tuple[int, int] = ...


class ConfigurableType(type):
    def __new__(cls, name, bases, namespace, **opts):
        namespace["_cfg_extra"] = opts or {}
        # namespace.update(opts)
        return super().__new__(cls, name, bases, namespace)


class BaseConfig(BaseModel, arbitrary_types_allowed=True):
    factory: QWidget = None
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

    def init_widget(self) -> QWidget:
        self.cfg = self.build_config()
        self.name = self.cfg.name
        self.widget = self.factory()
        setup_settings(self.widget, self.cfg)
        return self.widget

    def build_config(self):
        print(self._cfg_extra or {})
        return self.Config(**(self._cfg_extra or {}))

    def factory(self):
        return self.cfg.factory(*self.cfg.init_args, **self.cfg.init_kwargs)
