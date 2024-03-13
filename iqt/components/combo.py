from PySide6.QtWidgets import QWidget, QComboBox, QCompleter
from PySide6.QtCore import Qt

from iqt.components.base import BaseObject, BaseConfig


class ComboBoxWidget(QComboBox):
    empty_state: str

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentTextChanged.connect(self.empty_handler)
        self.setEditable(True)

    def set_items(self, texts, sort=True):
        self.clear()
        self.set_empty_state()
        self.add_items(texts, sort=sort)

    def add_items(self, texts, sort=True):
        if sort:
            texts = set(sorted(texts))
            texts = sorted(texts)
        else:
            texts = list(texts)

        completer = QCompleter(texts)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        self.setCompleter(completer)
        super(ComboBoxWidget, self).addItems(texts)

    def get_all_items(self):
        return [self.itemText(i) for i in range(self.count())]

    def set_text(self, text):
        index = -1 if text == self.empty_state else self.findText(text)
        self.setCurrentIndex(index)

    def clear_text(self):
        self.setCurrentIndex(-1)

    def set_empty_state(self, state=None):
        state = state or self.empty_state
        self.empty_state = state
        self.setPlaceholderText(state)
        self.lineEdit().setPlaceholderText(state)
        self.add_items([state])
        self.set_text(state)

    def empty_handler(self, text):
        if text == self.empty_state:
            self.setCurrentIndex(-1)


class ComboBoxConfig(BaseConfig):
    name: str = "combo_box"
    empty_state: str = " "


class ComboBox(BaseObject):
    Config = ComboBoxConfig
    to_connect: dict = {"items_handler": ["clicked"]}
    factory: QWidget = ComboBoxWidget
