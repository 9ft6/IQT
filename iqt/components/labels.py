from pathlib import Path

from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from iqt.components.base import BaseObject


Size: tuple[int, int] = ...


class BaseLabel(BaseObject, name="label"):
    factory: QWidget = QLabel


class Label(BaseLabel, fixed_height=16):
    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = text
        super().__init__(*args, **kwargs)


class Title(Label, name="title"):
    ...


class ImageLabel(QLabel):
    net_manager: QNetworkAccessManager

    def __init__(self, image, *args, **kwargs):
        self.set_image(image)
        super().__init__(*args, **kwargs)

    def load_from_web(self, image: str):
        self.net_manager = QNetworkAccessManager()
        self.net_manager.finished.connect(self.on_image_loaded)
        self.net_manager.get(QNetworkRequest(QUrl(image)))

    def on_image_loaded(self, reply):
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        scaled = pixmap.scaledToWidth(self.widget.width())
        self.widget.setPixmap(scaled)

    def set_image(self, image: str):
        if Path(image).exists():
            self.widget.setPixmap(QPixmap(image))
        elif QUrl(image).isValid():
            self.load_from_web(image)


class Image(BaseLabel, name="image"):
    factory: QWidget = ImageLabel

    def __init__(self, image, *args, **kwargs):
        kwargs["image"] = image
        super().__init__(*args, **kwargs)
