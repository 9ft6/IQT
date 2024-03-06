from PySide6.QtWidgets import QWidget, QPushButton
from iqt.components.base import BaseWidget, BaseConfig


class Button(BaseWidget):
    class Config(BaseConfig):
        name: str = "button"
        to_connect: dict = {"items_handler": ["clicked"]}

    factory: QWidget = QPushButton

    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = text
        super().__init__(*args, **kwargs)
