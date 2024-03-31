from copy import deepcopy
from typing import get_args, get_origin, Literal
from types import UnionType

from pydantic import BaseModel
from iqt.components.layouts import Horizont, Vertical
from iqt.components.widgets import CustomQWidget, Widget
from iqt.components.data_view.dataset.fields import (
    ComboBoxField,
    CheckBoxField,
    StringField,
    ListField,
    NameField,
    PreviewField,
    RowPreviewField,
    RowNameField,
    # DynamicSubItem,
)

name_label_width = 80


class BaseDataItem(BaseModel):
    _view_widgets: dict = {}
    _sort_fields: list = []
    id: str


class DynamicItemWidget(CustomQWidget):
    ...


class BaseDynamicItemWidget(Widget, name="base_item_widget"):
    factory = DynamicItemWidget
    layout = Vertical
    tail = []

    def __init__(self, item, layout_name, **kwargs):
        self.item = item
        self.layout_name = layout_name
        self._sub_widgets = getattr(item, "_sub_widgets", {})
        super().__init__()


class BaseDynamicItem(BaseDynamicItemWidget):
    def _prepare_widgets(self):
        widgets = []
        for name, field in self.item.__fields__.items():
            if widget := self._sub_widgets.get(name):
                widgets.append(widget(name, self.item, field))
            elif widget := self.get_widget_by_field(field):
                widgets.append(widget(name, self.item, field))

        return sorted(widgets, key=lambda x: x.order)

    def sub_item_handler(self, *args, **kwargs):
        print(args, kwargs)

    def generate_items(self, **kwargs):
        return self.layout[*self._prepare_widgets(), *self.tail]

    def get_widget_by_field(cls, f):
        if get_origin(f.annotation) is UnionType:
            field = deepcopy(f)
            field.annotation = [
                i for i in get_args(f.annotation)
                if i is not None.__class__
            ][0]
            return cls.get_widget_by_field(field)
        elif f.description and f.description.startswith('<') and f.description.endswith('>'):
            return cls.get_special_widget(f.description)
        elif get_origin(f.annotation) is Literal:
            return ComboBoxField
        elif f.annotation in {str, int, float}:
            return StringField
        elif f.annotation is bool:
            return CheckBoxField
        elif get_origin(f.annotation) is list and (args := get_args(f.annotation)):
            if len(set(args)) == 1 and type(args[0]) not in [str, int, float, bool]:
                return ListField
        # else:
        #     print(f"Unknown widget type: {f.annotation} {get_origin(f.annotation)}")

    @classmethod
    def get_special_widget(cls, widget_name):
        match widget_name:
            case "<preview>":
                return PreviewField
            case "<item_name>":
                return NameField


class DynamicFlowItem(BaseDynamicItem, fixed_width=250):
    layout_extra_settings = {"spacing": 0}


class DynamicColumnItem(BaseDynamicItem, fixed_width=250):
    tail = [...]


class DynamicRowItem(BaseDynamicItem):
    layout = Horizont

    @classmethod
    def get_special_widget(cls, widget_name):
        match widget_name:
            case "<preview>":
                return RowPreviewField
            case "<item_name>":
                return RowNameField


get_item_by_layout = {
    'flow': DynamicFlowItem,
    'vertical': DynamicRowItem,
    'horizont': DynamicColumnItem,
}.__getitem__

