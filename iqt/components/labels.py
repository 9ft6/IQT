from pathlib import Path

from PySide6.QtWidgets import QLabel, QWidget

from iqt.components.base import BaseObject, BaseConfig, BaseImageWidgetMixin


Size: tuple[int, int] = ...


class BaseLabel(BaseObject, name="label"):
    factory: QWidget = QLabel


class Label(BaseLabel, fixed_height=16):
    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = str(text)
        super().__init__(*args, **kwargs)


class Title(Label, name="title"):
    ...


class ImageLabel(QLabel, BaseImageWidgetMixin):
    ...


class Image(BaseLabel, name="image"):
    class Config(BaseConfig):
        image: str | Path

    factory: QWidget = ImageLabel

    def __init__(self, image, *args, **kwargs):
        kwargs["image"] = image
        super().__init__(*args, **kwargs)
