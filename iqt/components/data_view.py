from typing import Literal

from PySide6.QtWidgets import QWidget, QScrollArea, QScrollBar, QScroller, QScrollerProperties
from PySide6.QtCore import Qt, QEasingCurve

from iqt.components.base import BaseObject, BaseConfig
from iqt.components.widgets import Widget
from iqt.components.layouts import Horizont, Flow, Vertical


layouts = {
    "horizont": Horizont,
    "vertical": Vertical,
    "flow": Flow,
}
get_layout_by_type = layouts.__getitem__


class DataViewWidget(QScrollArea):
    name = "data_view"

    def setup_layout(self, config):
        size = self.parent().size()
        self.direction = config.direction

        class MainWidget(Widget, size=size.toTuple(), name="scroll_area_widget"):
            items = get_layout_by_type(config.direction)[None]

        self.scroll_widget = MainWidget().create_widget()
        self.layout = self.scroll_widget.layout()
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)

        if config.direction == 'horizontal':
            show_h_scroll, show_v_scroll = Qt.ScrollBarAsNeeded, Qt.ScrollBarAlwaysOff
            scroll_bar_setter = getattr(self, "setHorizontalScrollBar")
        else:
            show_h_scroll, show_v_scroll = Qt.ScrollBarAlwaysOff, Qt.ScrollBarAsNeeded
            scroll_bar_setter = getattr(self, "setVerticalScrollBar")

        self.scroll_bar = QScrollBar()
        self.setHorizontalScrollBarPolicy(show_h_scroll)
        self.setVerticalScrollBarPolicy(show_v_scroll)
        scroll_bar_setter(self.scroll_bar)
        self.scroller = self.setup_scroller()

    def add_widget(self, widget):
        self.layout.addWidget(widget.create_widget())
        self.auto_resize()

    def auto_resize(self):
        attrs = {"horizont": "width", "vertical": "height"}
        if attr_name := attrs.get(self.direction):
            value = 0
            if widget := self.layout.itemAt(0):
                count = self.layout.count()
                value = getattr(widget.widget(), attr_name)()
                value = count * value + (count + 1) * self.layout.spacing()

            method = getattr(self.scroll_widget, f"setFixed{attr_name.capitalize()}")
            method(value)

    def setup_scroller(self):
        scroller = QScroller.scroller(self.viewport())
        scroller.grabGesture(self.viewport(), QScroller.LeftMouseButtonGesture)
        properties = scroller.scrollerProperties()
        properties.setScrollMetric(QScrollerProperties.ScrollingCurve, QEasingCurve.OutCirc)
        properties.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.001)
        properties.setScrollMetric(QScrollerProperties.AxisLockThreshold, 0.6)
        properties.setScrollMetric(QScrollerProperties.DecelerationFactor, 0.10)
        properties.setScrollMetric(QScrollerProperties.DragStartDistance, 0.005)
        properties.setScrollMetric(QScrollerProperties.FrameRate, properties.FrameRates.Fps60)
        properties.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.6)
        properties.setScrollMetric(QScrollerProperties.OvershootDragResistanceFactor, 0.33)
        properties.setScrollMetric(QScrollerProperties.OvershootScrollDistanceFactor, 0.33)
        properties.setScrollMetric(QScrollerProperties.SnapPositionRatio, 0.90)
        return scroller


class DataView(BaseObject):
    class Config(BaseConfig):
        name: str = "data_view"
        direction: Literal["vertical", "horizont", "flow"] = "flow"

    factory: QWidget = DataViewWidget

    def __init__(self, name=None, *args, **kwargs):
        kwargs["name"] = name
        super().__init__(*args, **kwargs)

    def add(self, widget: BaseObject | list[BaseObject]):
        widgets = widget if isinstance(widget, list) else [widget]
        for widget in widgets:
            self.widget.add_widget(widget)

    def remove(self, num: int):
        ...

    def clear(self):
        ...

    def post_init(self) -> None:
        copy_methods = ["add", "remove", "clear"]
        for m in copy_methods:
            if v := getattr(self, m, None):
                setattr(self.widget, m, v)
        self.widget.setup_layout(self.cfg)

    def init_widget(self, parent=None):
        return self.factory(parent)
