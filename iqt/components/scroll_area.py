from PySide6.QtWidgets import QScrollArea, QScrollBar

from iqt.components.widgets import Widget
from iqt.components.layouts import Horizont, Flow, Vertical
from iqt.components.data_view.scroller import ScrollerMixin


get_layout_by_type = {
    "horizont": Horizont,
    "vertical": Vertical,
    "flow": Flow,
}.__getitem__


class DataViewScrollArea(QScrollArea, ScrollerMixin):
    name = "data_view"

    def setup_layout(self, config):
        self.cfg = config

        class MainWidget(Widget, name="scroll_area_widget"):
            items = get_layout_by_type(config.direction)[None]

        self.scroll_widget = MainWidget().create_widget()
        self.layout = self.scroll_widget.layout()
        self.setWidget(self.scroll_widget)

        self.scroll_bar = QScrollBar()
        self.setHorizontalScrollBarPolicy(self.cfg.h_scroll_policy)
        self.setVerticalScrollBarPolicy(self.cfg.v_scroll_policy)
        if scroll_bar_setter := getattr(self, self.cfg.scroll_bar_setter):
            scroll_bar_setter(self.scroll_bar)

        self.scroller = self.setup_scroller()

    def add_widget(self, widget):
        widget = widget.create_widget(self.scroll_widget)
        widget.setVisible(False)
        self.layout.addWidget(widget)
        widget.setVisible(True)
        self.auto_resize()

    def auto_resize(self):
        attrs = {"horizont": "width", "vertical": "height"}
        if attr_name := attrs.get(self.cfg.direction):
            value = 0
            if widget := self.layout.itemAt(0):
                count = self.layout.count()
                value = getattr(widget.widget(), attr_name)()
                value = count * value + (count + 1) * self.layout.spacing()

            method = getattr(self.scroll_widget, f"setFixed{attr_name.capitalize()}")
            method(value)

    def clear(self):
        while item := self.layout.itemAt(0):
            widget = item.widget()
            widget.hide()
            self.layout.removeWidget(widget)
