from pathlib import Path

from PySide6.QtWidgets import QPushButton, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

from iqt.components.base import BaseWidgetObject


class Button(
    BaseWidgetObject,
    signals={"items_handler": ["clicked"]}
):
    name: str = "button"
    factory: QWidget = QPushButton

    def __init__(self, text=None, **kwargs):
        self.text = str(text) if isinstance(text, (int, float)) else text
