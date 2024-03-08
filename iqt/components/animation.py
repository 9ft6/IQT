import subprocess
import platform

from PySide6.QtWidgets import (QPushButton, QLayout, QWidget, QComboBox, QCheckBox, QSlider, QToolTip, QTableWidget,
                               QGraphicsOpacityEffect, QLineEdit, QTextEdit, QApplication, QTableWidgetItem, QLabel,
                               QProgressBar, QStylePainter, QStyleOptionProgressBar, QStyle, QHBoxLayout, QCompleter,
                               QAbstractItemView, QScrollArea, QScroller, QScrollBar, QMainWindow, QStyledItemDelegate)
from PySide6.QtCore import (Qt, QPropertyAnimation, QSize, QRect, QPoint, Property, QTimer,
                            QAbstractAnimation, QEasingCurve, Signal, QPointF, QEvent)
from PySide6.QtGui import QIcon, QCursor, QAction, QFontMetrics, QStandardItem, QPalette, QColor




class BaseAnimation:
    effect = None
    full_opacity = 0.999999
    hover_opacity = 0.5
    click_opacity = 0.2
    duration = 150
    animated = True

    def set_animated(self, value):
        self.animated = value

    def enterEvent(self, event):
        self.start_hover_animation('Forward')

    def leaveEvent(self, event):
        self.start_hover_animation('Backward')

    def setup_click_fade_animation(self):
        if self.animated:
            self.click_animation = self.get_fade_animation(
                self.hover_opacity,
                self.hover_opacity,
                (0.5, self.click_opacity)
            )
            self.clicked.connect(self.start_click_animation)

    def setup_hover_fade_animation(self):
        if self.animated:
            self.hover_animation = self.get_fade_animation(self.full_opacity, self.hover_opacity, keys=None)

    def start_click_animation(self):
        if animation := getattr(self, 'click_animation', None):
            self.start_animation(animation, animation.Forward)

    def start_hover_animation(self, direction):
        if animation := getattr(self, 'hover_animation', None):
            self.start_animation(animation, direction)

    def get_fade_animation(self, start, end, keys=None, curve=None):
        if not self.effect:
            self.effect = QGraphicsOpacityEffect(opacity=self.full_opacity)
            self.setGraphicsEffect(self.effect)
        return self.get_property_animation(self.effect, b'opacity', start, end, self.duration, keys=keys, curve=curve)

    def get_property_animation(self, target, property, start, end, duration, keys=None, curve=None):
        animation = QPropertyAnimation(target, property, duration=duration, startValue=start, endValue=end)
        if curve:
            animation.setEasingCurve(curve)
        if keys:
            animation.setKeyValueAt(*keys)
        return animation

    def start_animation(self, animation, direction):
        if isinstance(direction, str):
            direction = getattr(animation, direction)
        animation.stop()
        animation.setDirection(direction)
        animation.start()


class BaseAnimatedResizeWidget(BaseAnimation):
    duration = 250
    resize_start, resize_ends = 0, 0
    resize_keys = (0.5, 0.5)
    curve = QEasingCurve.InOutExpo  # OutQuart  InOutQuart
    orientation = 'v'
    #
    # def __init__(self, parent, construct):
    #     super(BaseAnimatedResizeWidget, self).__init__(parent, construct)
    #     self.expanded = False
    #     self.size_value = 0
    #     self.orientation = 'v'
    #     self.scroll_area = getattr(self, f'scroll_area', None)

    @Property(int)
    def animated_size(self):
        return self.size_value

    @animated_size.setter
    def animated_size(self, value):
        self.set_method(self.size_value)
        self.size_value = value

    def animation_callback(self):
        self.set_method(self.resize_ends)

    def start_resize_animation(self, start, end):
        self.resize_start, self.resize_ends = start, end
        self.animation = None
        self.animation = self.get_move_animation(start, end, b'animated_size')
        self.animation.finished.connect(self.animation_callback)
        self.animation.start()

    def get_move_animation(self, start, end, property):
        if property == b'geometry':
            start = start if isinstance(start, QRect) else QRect(*start)
            end = end if isinstance(end, QRect) else QRect(*end)
        animation = QPropertyAnimation(
            self,
            property,
            duration=self.duration,
            startValue=start,
            endValue=end,
        )
        if self.curve:
            animation.setEasingCurve(self.curve)
        return animation

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.set_method = self.setFixedWidth if orientation == 'v' else self.setFixedHeight
        self.set_method(self.size_value)

    def expand(self):
        layout = self.scroll_area.main_layout
        hint = layout.sizeHint().toTuple()
        margins_h = sum([layout.contentsMargins().left(), layout.contentsMargins().right()])
        margins_v = sum([layout.contentsMargins().top(), layout.contentsMargins().bottom()])
        margins = margins_v if self.orientation == 'v' else margins_h
        width_hint = hint[0] if self.orientation == 'v' else hint[1]
        start = self.size().width() if self.orientation == 'v' else self.size().height()
        end = width_hint - margins if width_hint in [0, margins] else width_hint + margins
        if end < 30:
            end = 0
        else:
            end -= 10
        if self.resize_ends != end:
            self.start_resize_animation(start, end)

    def show_widget(self, id=''):
        for _id, widget in self.scroll_area.items.items():
            if _id == id:
                widget.show()
                self.expand()
            else:
                widget.hide()
                self.expand()

    def remove_widget(self, widget):
        self.scroll_area.remove_widget(widget)
        self.expand()

    def add_widget(self, widget):
        self.scroll_area.add_widget(widget)
        self.expand()

    def add_stretch(self):
        self.scroll_area.add_stretch()

    def clear(self):
        self.scroll_area.clear()
        self.expand()
