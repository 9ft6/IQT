from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QCursor
from PySide6.QtCore import QEvent, QSize, Qt

from iqt.components.animation import (
    AnimatedWidgetMixin,
    BaseAnimation,
    ShowHideFadeAnimation,
)
from iqt.components.layouts import Horizont
from iqt.components.widgets import CustomQWidget, Widget
from iqt.events import ClosePopupEvent


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


class PopupWidget(CustomQWidget, AnimatedWidgetMixin):
    old_pos = None
    old_size = None
    effect = None
    animations: list[BaseAnimation] = [ShowHideFadeAnimation]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = ResizeLabel(self)

    def resizeEvent(self, event):
        self._update_size()

    def _update_size(self):
        if current := self.entity.current:
            pos = self.size() / 2 - current.size() / 2
            current.move(*pos.toTuple())
            x, y = (current.geometry().size() + pos).toTuple()
            w, h = self.label.size().toTuple()
            self.label.move(x - w + 2, y - h + 2)

    def eventFilter(self, watched, event):
        if not (current := self.entity.current):
            return super().eventFilter(watched, event)

        match event.type():
            case QEvent.MouseButtonPress | QEvent.MouseButtonDblClick:
                pos = event.pos()
                outside_current = not current.geometry().contains(pos)
                outside_label = not self.label.geometry().contains(pos)
                if outside_current and outside_label:
                    self.entity.send_event(ClosePopupEvent())

                diff = (current.geometry().bottomRight() - pos)
                if all(x < 10 for x in diff.toTuple()):
                    self.old_pos = pos
                    self.old_size = current.size()
            case QEvent.MouseMove:
                if self.old_pos:
                    diff = ((event.pos() - self.old_pos) * 2).toTuple()
                    new_size = self.old_size + QSize(*diff)
                    current.resize(*new_size.toTuple())
                    self._update_size()
            case QEvent.MouseButtonRelease:
                if self.old_pos:
                    self.old_pos = None

        return super().eventFilter(watched, event)

    def hide(self):
        if self.is_animated:
            self.fade_out()
        else:
            super().hide()

    def show(self):
        super().show()
        self._update_size()
        self.fade_in()


class Popup(Widget, name="popup"):
    class Config(Widget.Config):
        event_filter: bool = True
        animated: bool = True

    factory = PopupWidget
    items = Horizont[...]
    current: Widget

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current = None

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
            case "open_popup" | "set_popup":
                if self.current:
                    self.widget.layout().removeWidget(self.current)
                    self.current.deleteLater()
                    self.current = None

                self.current = message.message().create_widget(self.widget)
                self.widget.show()
