from typing import Any

from iqt.components.data_view.data_view import (
    FlowDataView,
    VerticalDataView,
    HorizontDataView,
    BaseDataView,
)
from iqt.components.buttons import FlowBtn, HorizontBtn, VerticalBtn
from iqt.components.data_view.dataset.item import BaseDataItem, get_item_by_layout
from iqt.components.data_view.navigation.pagination import Pagination
from iqt.components.data_view.navigation.sort import SortingWidget
from iqt.components.data_view.navigation.filter import FilterWidget
from iqt.components.data_view.popup import Popup
from iqt.components.data_view.dataset.ds import Dataset
from iqt.components.layouts import Vertical, Horizont
from iqt.components.widgets import CustomQWidget, Widget

from iqt.logger import logger


class NavBar(Widget, name="navbar"):
    def __init__(self, dataview, *args, **kwargs):
        self.dataview = dataview
        super().__init__(*args, **kwargs)

    def generate_items(self):
        return Horizont[
            ...,
            Pagination(self.dataview),
            ...,
            Horizont[
                SortingWidget(self.dataview),
                FilterWidget(self.dataview)
            ],
            FlowBtn(),
            HorizontBtn(),
            VerticalBtn(),
        ]


class DynamicDataViewWidget(CustomQWidget):
    def show_filter(self):
        from PySide6.QtWidgets import QLabel
        button = QLabel(self)
        button.setText("some")
        button.move(10, 10)

    def resizeEvent(self, event):
        if self.entity.popup:
            self.entity.popup.resize(event.size())
        self.show_filter()
        return super().resizeEvent(event)


available_view_types = ["flow", "vertical", "horizont"]


class DynamicDataView(Widget):
    factory = DynamicDataViewWidget
    to_connect = {
        "view_type_handler": [
            "navbar.flow.clicked",
            "navbar.vertical.clicked",
            "navbar.horizont.clicked",
        ],
    }
    item_model: BaseDataItem
    active: BaseDataView
    popup: Widget
    dataset: Dataset
    pagination: Pagination
    no_popup: bool = False

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.active: BaseDataView = None
        self.popup: Widget = None

    def generate_items(self):
        return Vertical[
            NavBar(self),
            FlowDataView("flow", hidden=True),
            VerticalDataView("vertical", hidden=True),
            HorizontDataView("horizont", hidden=True),
        ]

    def event_bus_handler(self, message):
        if str(id(self)) == message.target:
            self.widget.show_filter()

    def post_init(self):
        for name in available_view_types:
            if name in self.cfg.ignore_view_types:
                continue

            if view := getattr(self.navbar, name, None):
                view.show()

        if not self.no_popup:
            self.popup = Popup().create_widget(parent=self.widget)

        self.dataset = self.dataset(self.update_content)
        self.pagination = self.navbar.pagination
        self.sorting = self.navbar.sorting
        self.filter = self.navbar.filter

        for v_type in available_view_types:
            if v_type not in self.cfg.ignore_view_types:
                self.ensure_type_btn(v_type, v_type)
                break

        self.update_content()

    def update_content(self):
        self.active.clear()
        for item in self.dataset:
            widget = None
            try:
                view_widgets = self.item_model.view_widgets
                widget = view_widgets.get(self.active.name, None)
            except Exception as e:
                logger.error(f"While custom item widget: {e}")

            if not widget:
                widget = get_item_by_layout(self.active.name)

            self.active.add(widget(item, self.active.name))

        self.pagination.entity.update()
        self.sorting.entity.update()

    def view_type_handler(self, sender, *args, **kwargs):
        for name in available_view_types:
            self.ensure_type_btn(name, sender.name)

        self.update_content()

    def ensure_type_btn(self, name, sender_name):
        if view := getattr(self, name, None):
            view.setHidden(name != sender_name)
            if name == sender_name:
                self.active = view
