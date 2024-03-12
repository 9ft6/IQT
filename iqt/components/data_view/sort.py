from iqt.components.base import BaseConfig
from iqt.components import Widget, ComboBox
from iqt.components.layouts import Horizont
from iqt.components.combo import ComboBoxConfig


class SortingComboBox(ComboBox):
    class Config(ComboBoxConfig):
        empty_state: str = "Sorting key"
        name: str = "sort_box"
        fixed_width: int = 128


class SortingConfig(BaseConfig):
    name: str = 'sorting'


class SortingWidget(Widget):
    Config = SortingConfig
    items = Horizont[SortingComboBox()]
    to_connect: dict[str, list[str]] = {
        "sort_handler": [
            "sort_box.currentTextChanged"
        ]
    }

    def update(self):
        self.sort_box.add_items(self.widget.dataset.get_sort_fields())

    def sort_handler(self, sender, text):
        value = text if sender.empty_state != text else None
        self.widget.dataset.set_sort_key(value)
