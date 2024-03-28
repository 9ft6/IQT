from iqt.components.layouts import Vertical, Horizont
from iqt.components.data_view.item import BaseDataItem, get_item_by_layout
from iqt.components.data_view.pagination import Pagination
from iqt.components.data_view.sort import SortingWidget
from iqt.components.data_view.filter import FilterWidget
from iqt.components import (
    Widget,
    FlowDataView,
    VerticalDataView,
    HorizontDataView,
    BaseDataView,
)
from iqt.components.data_view.dataset import Dataset
from iqt.components.buttons import FlowBtn, HorizontBtn, VerticalBtn


class EditSideBar(Widget, fixed_width=132):
    items = Vertical[...]


class NavBar(Widget, name="navbar"):
    items = Horizont[
        FlowBtn(),
        HorizontBtn(),
        VerticalBtn(),
        ...,
        Pagination(),
        ...,
        Horizont[FilterWidget()],
        Horizont[SortingWidget()],
    ]


class DynamicDataView(Widget):
    items = Vertical[
        # EditSideBar(),
        NavBar(),
        FlowDataView("flow", hidden=True),
        VerticalDataView("vertical", hidden=True),
        HorizontDataView("horizont", hidden=True),
    ]
    to_connect = {
        "view_type_handler": [
            "navbar.flow.clicked",
            "navbar.vertical.clicked",
            "navbar.horizont.clicked",
        ],
    }
    item_model: BaseDataItem
    active: BaseDataView = None
    dataset: Dataset
    pagination: Pagination

    def post_init(self):
        for name in ["flow", "vertical", "horizont"]:
            if view := getattr(self.navbar, name, None):
                view.show()

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
                widget = self.item_model._view_widgets.get(self.active.name, None)
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
