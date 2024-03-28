from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QEvent, QSize, Qt
from PySide6.QtGui import QCursor

from iqt.components import Widget
from iqt.events import ClosePopupEvent
from iqt.components.layouts import Horizont
from iqt.components.widgets import CustomQWidget


class ResizeLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.setObjectName("popup_resize_label")
        self.setFixedSize(10, 10)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Enter:
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif event.type() == QEvent.Leave:
            self.unsetCursor()
        return super().eventFilter(watched, event)


class PopupWidget(CustomQWidget):
    old_pos = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize_label = ResizeLabel(self)

    def resizeEvent(self, event):
        if current := self.entity.current:
            pos = event.size() / 2 - current.geometry().size() / 2
            current.move(*pos.toTuple())
            x, y = (current.geometry().size() + pos).toTuple()
            w, h = self.resize_label.size().toTuple()
            self.resize_label.move(x - w + 2, y - h + 2)

    def eventFilter(self, watched, event):
        if not (current := self.entity.current):
            return super().eventFilter(watched, event)

        match event.type():
            case QEvent.MouseButtonPress | QEvent.MouseButtonDblClick:
                diff = current.geometry().bottomRight() - event.pos()
                if all(x < 10 for x in diff.toTuple()):
                    self.old_pos = event.pos()
                    self.old_size = current.size()
            case QEvent.MouseMove:
                if self.old_pos:
                    diff = event.pos() - self.old_pos
                    new_size = self.old_size + QSize(*(diff * 2).toTuple())
                    current.resize(*new_size.toTuple())
                    self.entity.move_to_center(current)
            case QEvent.MouseButtonRelease:
                if self.old_pos:
                    self.old_pos = None
                else:
                    if not current.geometry().contains(event.pos()):
                        self.entity.send_event(ClosePopupEvent())

        return super().eventFilter(watched, event)


class Popup(Widget, name="popup"):
    class Config(Widget.Config):
        event_filter: bool = True

    factory = PopupWidget
    items = Horizont[...]
    current: Widget = None

    def post_init(self):
        self.widget.resize(self.widget.parent().size())
        self.widget.hide()

    def event_bus_handler(self, message):
        if message.target != "popup":
            return

        match message.type:
            case "close_popup":
                self.widget.hide()
                if self.current:
                    self.current.hide()
                    # self.widget.clear()
            case "open_popup" | "set_popup":
                if self.current:
                    self.widget.layout().removeWidget(self.current)

                self.current = message.message().create_widget(self.widget)
                self.move_to_center(self.current)
                self.widget.show()

    def move_to_center(self, widget):
        pos = self.widget.geometry().size() / 2 - widget.geometry().size() / 2
        widget.move(*pos.toTuple())
