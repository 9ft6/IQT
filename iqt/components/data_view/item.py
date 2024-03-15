from copy import deepcopy
from typing import get_args, get_origin, Literal
from types import UnionType

from pydantic import BaseModel

from iqt.images import svg
from iqt.components import Widget, Label, Image, ComboBox, Title, Input, ImageLabel
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
        value = str(getattr(self.item, self.name, ""))
        return Horizont[
            Label(self.field.description, fixed_width=64),
            Input(name=f"_{self.name}", text=value)
        ]


class PreviewLabel(ImageLabel):
    def load_from_web(self, image: str):
        super().load_from_web(image)
        self.setFixedWidth(self.parent().parent().width())
        self.set_image(svg.no_preview)


class Preview(Image):
    factory = PreviewLabel


class PreviewField(BaseFieldWidget):
    order: int = 2

    def generate_items(self):
        return Horizont[Preview(getattr(self.item, self.name, None))]


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


class BaseDataItem(BaseModel):
    _view_widgets: dict
    id: str
    slug: str


class DynamicItemWidget(CustomQWidget):
    ...


class BaseDynamicItem(Widget, name="base_item_widget"):
    factory = DynamicItemWidget
    layout = Vertical
    tail = []

    def __init__(self, item, layout_name, **kwargs):
        self.item = item
        self.layout_name = layout_name
        super().__init__()

    def _prepare_widgets(self):
        widgets = []
        for name, field in self.item.__fields__.items():
            if widget := self.get_widget_by_field(field):
                widgets.append(widget(name, self.item, field))

        return sorted(widgets, key=lambda x: x.order)

    def generate_items(self, **kwargs):
        return self.layout[*self._prepare_widgets(), *self.tail]

    @classmethod
    def get_widget_by_field(cls, f):
        if get_origin(f.annotation) is UnionType:
            field = deepcopy(f)
            field.annotation = [i for i in get_args(f.annotation) if i is not None.__class__][0]
            return cls.get_widget_by_field(field)
        elif f.description and f.description.startswith('<') and f.description.endswith('>'):
            return cls.get_special_widget(f.description)
        elif get_origin(f.annotation) is Literal:
            return ComboBoxField
        elif f.annotation in {str, int, float}:
            return StringField
        elif f.annotation is bool:
            ...  # TODO: implement and return "check_box"
        else:
            print(f"Unknown widget type: {f.annotation}")

    @classmethod
    def get_special_widget(cls, widget_name):
        match widget_name:
            case "<preview>":
                return PreviewField
            case "<item_name>":
                return NameField


class DynamicFlowItem(BaseDynamicItem, fixed_width=250):
    ...


class DynamicColumnItem(BaseDynamicItem, fixed_width=250):
    tail = [...]


class RowNameField(BaseFieldWidget):
    order: int = 2

    def generate_items(self):
        return Horizont[Label(getattr(self.item, self.name, None), fixed_width=160)]


class RowPreviewField(BaseFieldWidget):
    order: int = 1

    def generate_items(self):
        return Horizont[Image(getattr(self.item, self.name, None), fixed_size=(160, 120))]


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
