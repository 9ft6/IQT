from typing import Any, Literal

from PySide6.QtWidgets import QGraphicsOpacityEffect
from PySide6.QtCore import (
    QPropertyAnimation,
    QAbstractAnimation,
    QEasingCurve,
    QObject,
    QRect,
    Property,
)

Direction = Literal['top', 'bottom', 'left', 'right']


class BaseAnimation:
    name: str
    property: bytes
    duration: int
    start: Any
    end: Any
    curve: QEasingCurve = None
    keys: list[tuple[float, float]] = None

    _target: QObject
    target: QObject

    def __init__(self, target: QObject) -> None:
        self._target = target
        self.setup(target)

    def setup(self, target: QObject) -> None:
        ...


class OpacityAnimation(BaseAnimation):
    def setup(self, target: QObject) -> None:
        if not target.effect:
            target.effect = QGraphicsOpacityEffect(opacity=1.0)
            target.setGraphicsEffect(target.effect)

        self.animation = target.get_property_animation(self)
        target.animation_callback = self.animation_callback
        self.animation.finished.connect(self.animation_callback)
        self.animation.finished.connect(target.fade_in_out_callback)
        self.target = self._target.effect

        setattr(target, f"{self.name}_animation", self.animation)

    def animation_callback(self):
        backward = QAbstractAnimation.Direction.Backward
        if self.animation.direction() == backward:
            try:
                self._target._hide()
            except:
                ...
        else:
            self._target._show()


class ShowHideFadeAnimation(OpacityAnimation):
    name: str = 'show_fade'
    property: bytes = b'opacity'
    duration: int = 160
    start: Any = 0.0
    end: Any = 1.0

    show_fade_animation: QPropertyAnimation


class ResizeAnimation(BaseAnimation):
    duration = 250
    property: bytes = b'geometry'
    start = 0
    end = 0
    keys = (0.5, 0.5)
    curve = QEasingCurve.InOutExpo  # OutQuart  InOutQuart

    def setup(self, target: QObject) -> None:
        self.start = self.start if isinstance(self.start, QRect) else QRect(*self.start)
        self.end = self.end if isinstance(self.end, QRect) else QRect(*self.end)
        self.target = target
        self.resize_animation = target.get_property_animation(self)
        print(self.resize_animation)


class AnimatedWidgetMixin:
    is_animated = True
    animations: list[BaseAnimation] = []

    def set_animated(self, value):
        self.is_animated = value
        if value:
            [animation(self) for animation in self.animations]

    def get_property_animation(self, animation: BaseAnimation):
        animation_ = QPropertyAnimation(
            animation._target.effect,
            animation.property,
            duration=animation.duration,
            startValue=animation.start,
            endValue=animation.end
        )
        if animation.keys:
            animation_.setKeyValueAt(*animation.keys)
        if animation.curve:
            animation_.setEasingCurve(animation.curve)
        return animation_

    def start_animation(self, animation, direction):
        if isinstance(direction, str):
            direction = getattr(QPropertyAnimation.Direction, direction)

        animation.stop()
        animation.setDirection(direction)
        animation.start()

    # Show fade animation methods
    def fade_in(self):
        if animation := getattr(self, 'show_fade_animation', None):
            self.start_animation(animation, 'Forward')
            return animation

    def fade_out(self):
        if animation := getattr(self, 'show_fade_animation', None):
            self.start_animation(animation, 'Backward')
            return animation

    def fade_in_out_callback(self):
        ...

    direction: Direction = "right"

    # Resize animation methods
    @Property(int)
    def animated_size(self):
        return self.size_value

    @animated_size.setter
    def animated_size(self, value):
        self.resize_set_method(self.size_value)
        self.size_value = value

    def animation_callback(self):
        self.resize_set_method(self.resize_ends)

    def resize_set_method(self, value):
        if self.direction in ['left', 'right']:
            self.setWidth(value)
        else:
            self.setHeight(value)
