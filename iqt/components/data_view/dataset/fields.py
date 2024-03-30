from typing import get_args

from iqt.images import svg
from iqt.components import (
    Label,
    Image,
    ComboBox,
    Title,
    Input,
    ImageLabel,
    CheckBox,
    Button,
    Widget,
)
from iqt.components.layouts import Horizont
from iqt.events import OpenPopupEvent

name_label_width = 80


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
        name = self.field.description or self.name
        return Horizont[
            Label(name, fixed_width=name_label_width),
            Input(name=f"_{self.name}", text=value)
        ]


class PreviewLabel(ImageLabel):
    def load_from_web(self, image: str):
        super().load_from_web(image)
        width = self.parent().parent().width() - 16
        self.setFixedWidth(width)
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


class ListField(BaseFieldWidget):
    order: int = 10

    def generate_items(self):
        value = getattr(self.item, self.name, None)
        name = f"{self.field.description or self.name}"
        return Horizont[Button(f"{name} ({len(value)})")]

    def items_handler(self, *args, **kwargs):
        value = getattr(self.item, self.name, None)
        if not value:
            return

        from iqt.components.data_view.dynamic import DynamicDataView
        from iqt.components.data_view.dataset import Dataset

        class GeneratedDataset(Dataset):
            initial_load: bool = False
            item_model = value[0]

            def __init__(self, update_callback=None):
                super().__init__(update_callback=update_callback)
                self.items = {i.id: i for i in value}

        class DataView(DynamicDataView, size=(800, 600)):
            item_model = value[0]
            dataset = GeneratedDataset
            no_popup = True

        self.send_event(OpenPopupEvent(DataView))


class ComboBoxField(BaseFieldWidget):
    def generate_items(self):
        name = self.field.description or self.name
        return Horizont[
            Label(self.field.description, fixed_width=name_label_width),
            ComboBox(
                empty_state=name,
                items=get_args(self.field.annotation),
                value=getattr(self.item, self.name, None)
            ),
        ]


class CheckBoxField(BaseFieldWidget):
    def generate_items(self):
        name = self.field.description or self.name
        return Horizont[CheckBox(text=name)]


class RowNameField(BaseFieldWidget):
    order: int = 2

    def generate_items(self):
        return Horizont[Label(getattr(self.item, self.name, None), fixed_width=160)]


class RowPreviewField(BaseFieldWidget):
    order: int = 1

    def generate_items(self):
        return Horizont[Image(getattr(self.item, self.name, None), fixed_size=(160, 120))]


class DynamicSubItem(BaseFieldWidget):
    order: int = 3

