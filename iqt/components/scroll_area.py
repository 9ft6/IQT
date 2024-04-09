from PySide6.QtWidgets import QScrollArea, QScrollBar, QWidgetItem

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
        self.stretch = None
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

        if self.cfg.direction != "flow":
            self.remove_stretch()
            self.layout.addWidget(widget)
            self.add_stretch()
        else:
            self.layout.addWidget(widget)

        widget.setVisible(True)

    def clear(self):
        while item := self.layout.itemAt(0):
            item.widget().setVisible(False)
            self.layout.removeItem(item)

    def add_stretch(self):
        self.layout.addStretch()

    def remove_stretch(self):
        if self.layout.count():
            if item := self.layout.itemAt(self.layout.count() - 1):
                self.layout.removeItem(item)
