from pathlib import Path

from iqt.components.layouts import Vertical, Horizont
from iqt.components.data_view.item import BaseDataItem
from iqt.components.base import BaseConfig
from iqt.components import (
    Button,
    Widget,
    FlowDataView,
    VerticalDataView,
    HorizontDataView,
    BaseDataView,
    ImageButton
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
        Button("pagination"),
        ...,
        Button("querying"),
        Button("sorting"),
    ]


class DynamicDataConfig(BaseConfig):
    ...


class DynamicDataView(Widget):
    class Config(DynamicDataConfig):
        ...

    items = Vertical[
        # EditSideBar(),
        NavBar(),
        ...,
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
    
    def post_init(self):
        for name in ["flow", "vertical", "horizont"]:
            if self.item_model.view_widgets.get(name):
                if view := getattr(self.navbar, name, None):
                    view.show()

        self.dataset = self.dataset()
        self.ensure_type_btn("flow", "flow")
        self.update_context()
        print(self.dataset)

    def update_context(self):
        for item in self.dataset:
            widget = self.item_model.view_widgets.get(self.active.name)
            self.active.add(widget(item))

    def view_type_handler(self, sender, *args, **kwargs):
        for name in ["flow", "vertical", "horizont"]:
            self.ensure_type_btn(name, sender.name)

        self.update_context()

    def ensure_type_btn(self, name, sender_name):
        if view := getattr(self, name, None):
            view.setHidden(name != sender_name)
            if name == sender_name:
                self.active = view
