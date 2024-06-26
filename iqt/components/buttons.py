from pathlib import Path

from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtGui import QIcon, Qt, QPixmap

from iqt.images import svg
from iqt.components.base import BaseObject, BaseConfig, BaseImageWidgetMixin


class ButtonQWidget(QPushButton):
    ...


class ButtonConfig(BaseConfig):
    name: str = "button"
    text: str = ""
    image: str | Path = None


class Button(BaseObject):
    Config = ButtonConfig

    to_connect: dict = {"items_handler": ["clicked"]}
    factory: QWidget = ButtonQWidget

    def __init__(self, text=None, *args, **kwargs):
        extra = self._cfg_extra
        kwargs["text"] = text or kwargs.get("text") or extra.get("text", "")
        super().__init__(*args, **kwargs)


class Submit(Button):
    class Config(ButtonConfig):
        name: str = "submit"
        shortcut: str = "Return"


class BaseImageButton(QPushButton, BaseImageWidgetMixin):
    def setPixmap(self, image):
        # self.setIcon(QIcon(image))
        scaled_pixmap = QPixmap(image).scaled(self.size(), Qt.KeepAspectRatio,
                                      Qt.SmoothTransformation)
        icon = QIcon(scaled_pixmap)
        self.setIcon(icon)
        self.setIconSize(self.size())


class ImageButton(Button):
    Config = ButtonConfig
    factory: QWidget = BaseImageButton

    def __init__(self, image=None, *args, **kwargs):
        if image:
            kwargs["image"] = image
        super().__init__(*args, **kwargs)


class ViewBtnConfig(ButtonConfig):
    hidden: bool = True
    fixed_size: tuple[int, int] = (18, 18)


class FlowBtn(ImageButton):
    class Config(ViewBtnConfig):
        name: str = "flow"
        image: str | Path = svg.flow


class HorizontBtn(ImageButton):
    class Config(ViewBtnConfig):
        name: str = "vertical"
        image: str | Path = svg.vertical


class VerticalBtn(ImageButton):
    class Config(ViewBtnConfig):
        name: str = "horizont"
        image: str | Path = svg.horizont


class AcceptBtn(Button, name="accept", text="Accept", default=True):
    ...


class DeclineBtn(Button, name="decline", text="Decline"):
    ...
