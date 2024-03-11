from pathlib import Path

from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QIcon

from iqt.images import svg
from iqt.components.base import BaseObject, BaseConfig, BaseImageWidgetMixin


class ButtonConfig(BaseConfig):
    name: str = "button"
    text: str = ""
    image: str | Path = None


class Button(BaseObject):
    Config = ButtonConfig

    to_connect: dict = {"items_handler": ["clicked"]}
    factory: QWidget = QPushButton

    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = text or ""
        super().__init__(*args, **kwargs)


class BaseImageButton(QPushButton, BaseImageWidgetMixin):
    def setPixmap(self, image):
        self.pixmap_path = f'images:{image}'
        self.setIcon(QIcon(self.pixmap_path))


class ImageButton(Button):
    Config = ButtonConfig
    factory: QWidget = BaseImageButton

    def __init__(self, image=None, *args, **kwargs):
        if image:
            kwargs["image"] = image
        super().__init__(*args, **kwargs)


class FlowBtn(ImageButton):
    class Config(ButtonConfig):
        name: str = "flow"
        image: str | Path = svg.a
        hidden: bool = True


class HorizontBtn(ImageButton):
    class Config(ButtonConfig):
        name: str = "vertical"
        image: str | Path = svg.b
        hidden: bool = True


class VerticalBtn(ImageButton):
    class Config(ButtonConfig):
        name: str = "horizont"
        image: str | Path = svg.c
        hidden: bool = True
