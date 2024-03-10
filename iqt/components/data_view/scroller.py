from PySide6.QtWidgets import QScroller, QScrollerProperties
from PySide6.QtCore import QEasingCurve


class ScrollerMixin:
    def _set_scroller_props(self, scroller: QScroller) -> None:
        properties = scroller.scrollerProperties()
        for name, value in {
            "ScrollingCurve": QEasingCurve.OutCirc,
            "DragVelocitySmoothingFactor": 0.001,
            "AxisLockThreshold": 0.6,
            "DecelerationFactor": 0.10,
            "DragStartDistance": 0.005,
            "FrameRate": properties.FrameRates.Fps60,
            "MaximumVelocity": 0.6,
            "OvershootDragResistanceFactor": 0.33,
            "OvershootScrollDistanceFactor": 0.33,
            "SnapPositionRatio": 0.90,
        }.items():
            property = getattr(QScrollerProperties, name)
            properties.setScrollMetric(property, value)

    def setup_scroller(self):
        scroller = QScroller.scroller(self.viewport())
        scroller.grabGesture(self.viewport(), QScroller.LeftMouseButtonGesture)
        self._set_scroller_props(scroller)
        return scroller
