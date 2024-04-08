from iqt.components.base import BaseObject

from PySide6.QtWidgets import QWidget, QTextEdit


class TextEdit(BaseObject, name="text"):
    factory: QWidget = QTextEdit

    def __init__(self, text=None, *args, **kwargs):
        kwargs["text"] = str(text)
        super().__init__(*args, **kwargs)
