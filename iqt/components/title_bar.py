from PySide6.QtCore import QEvent
from iqt.components.widgets import Widget, CustomQWidget
from iqt.components.buttons import Button
from iqt.components.layouts import Horizont


class TitleBarWidget(CustomQWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(16, 0)
        self.installEventFilter(self)
        self.setProperty("active", False)
        self.setObjectName("title_bar")

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Enter:
            self.set_active(True)
        elif event.type() == QEvent.Leave:
            self.set_active(False)
        return super().eventFilter(watched, event)

    def set_active(self, value: bool):
        self.setProperty("active", value)
        self.setStyle(self.style())


class TitleBar(Widget, name="title_bar"):
    factory = TitleBarWidget
    items = Horizont[
        Button("_"),
        Button("O"),
        Button("X"),
    ]
