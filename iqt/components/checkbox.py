from PySide6.QtWidgets import QWidget, QCheckBox

from iqt.components.base import BaseObject, BaseConfig


class CheckBoxWidget(QCheckBox):
    ...


class CheckBoxConfig(BaseConfig):
    name: str = "check_box"


class CheckBox(BaseObject):
    Config = CheckBoxConfig
    to_connect: CheckBoxConfig = {"items_handler": ["clicked"]}
    factory: QWidget = CheckBoxWidget
