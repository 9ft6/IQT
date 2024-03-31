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


class EditSideBar(Widget, fixed_width=132):
    items = Vertical[...]


class NavBar(Widget, name="navbar"):
    def generate_items(self):
        return Horizont[
            ...,
            Pagination(),
            ...,
            Horizont[FilterWidget()],
            Horizont[SortingWidget()],
            FlowBtn(),
            HorizontBtn(),
            VerticalBtn(),
        ]


class DynamicDataViewWidget(CustomQWidget):
    def resizeEvent(self, event):
        if self.entity.popup:
            self.entity.popup.resize(event.size())

        return super().resizeEvent(event)


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
            # EditSideBar(),
            NavBar(),
            FlowDataView("flow", hidden=True),
            VerticalDataView("vertical", hidden=True),
            HorizontDataView("horizont", hidden=True),
        ]

    def post_init(self):
        for name in ["flow", "vertical", "horizont"]:
            if name in self.cfg.ignore_view_types:
                continue

            if view := getattr(self.navbar, name, None):
                view.show()

        if not self.no_popup:
            self.popup = Popup().create_widget(parent=self.widget)

        self.dataset = self.dataset(self.update_content)
        self.pagination = self.navbar.pagination
        self.sorting = self.navbar.sorting
        self.sorting.dataset = self.dataset
        self.sorting.item_model = self.item_model

        self.pagination.dataset = self.dataset
        self.ensure_type_btn("flow", "flow")
        self.update_content()

    def update_content(self):
        self.active.clear()
        for item in self.dataset:
            widget = None
            try:
                view_widgets = self.item_model._view_widgets
                widget = view_widgets.get(self.active.name, None)
            except:
                ...

            if not widget:
                widget = get_item_by_layout(self.active.name)

            self.active.add(widget(item, self.active.name))

        self.pagination.entity.update()
        self.sorting.entity.update()

    def view_type_handler(self, sender, *args, **kwargs):
        for name in ["flow", "vertical", "horizont"]:
            self.ensure_type_btn(name, sender.name)

        self.update_content()

    def ensure_type_btn(self, name, sender_name):
        if view := getattr(self, name, None):
            view.setHidden(name != sender_name)
            if name == sender_name:
                self.active = view
