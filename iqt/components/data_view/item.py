from pydantic import BaseModel
from typing import Union, get_args, get_origin, Literal

from iqt.components import Widget, Label, Image, Title, ComboBox
from iqt.components.layouts import Horizont, Vertical
from iqt.components.widgets import CustomQWidget


class BaseFieldWidget(Widget):
    order: int = 10

    def __init__(self, name, item, field, **kwargs):
        self.name = name
        self.item = item
        self.field = field
        super().__init__(**kwargs)


class StringField(BaseFieldWidget):
    def generate_items(self):
        return Horizont[
            Label(self.field.description),
            Label(getattr(self.item, self.name, None))
        ]


class PreviewField(BaseFieldWidget):
    order: int = 2

    def generate_items(self):
        return Horizont[Image(getattr(self.item, self.name, None))]


class NameField(BaseFieldWidget):
    order: int = 1

    def generate_items(self):
        return Horizont[Title(getattr(self.item, self.name, None))]


class ComboBoxField(BaseFieldWidget):
    def generate_items(self):
        return Horizont[ComboBox(
            empty_state=self.field.description,
            set_items=get_args(self.field.annotation),
            default_value=getattr(self.item, self.name, None)
        )]


def get_special_widget(widget_name):
    match widget_name:
        case "<preview>":
            return PreviewField
        case "<item_name>":
            return NameField


def get_widget_by_field(f):
    if f.annotation is Union:
        return [i for i in get_args(f.annotation) if i is not None.__class__]
    elif f.description and f.description.startswith('<') and f.description.endswith('>'):
        return get_special_widget(f.description)
    elif get_origin(f.annotation) is Literal:
        return ComboBoxField
    elif f.annotation in {str, int, float}:
        return StringField
    elif f.annotation is bool:
        ...  # return "check_box"


class BaseDataItem(BaseModel):
    _view_widgets: dict
    id: str
    slug: str


class DynamicItemWidget(CustomQWidget):
    ...


class DynamicItem(Widget, name="base_item_widget"):
    factory = DynamicItemWidget

    def __init__(self, item, **kwargs):
        self.item = item
        super().__init__()

    def generate_items(self, **kwargs):
        widgets = []
        for name, field in self.item.__fields__.items():
            if widget := get_widget_by_field(field):
                widgets.append(widget(name, self.item, field))

        return Vertical[*sorted(widgets, key=lambda x: x.order)]
