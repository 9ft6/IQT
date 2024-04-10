from pathlib import Path

from iqt.components.widgets import Widget
from iqt.components.combo import ComboBox
from iqt.components.labels import Label
from iqt.components.layouts import Horizont
from iqt.components.combo import ComboBoxConfig
from iqt.components.buttons import ButtonConfig, ImageButton
from iqt.images import svg


class SortingComboBox(ComboBox):
    class Config(ComboBoxConfig):
        empty_state: str = "Sorting key"
        name: str = "sort_box"
        fixed_width: int = 128


class AscendingButton(ImageButton):
    class Config(ButtonConfig):
        name: str = "ascending_btn"
        image: str | Path = svg.ascending
        fixed_size: tuple[int, int] = (20, 20)


class SortingWidget(Widget, name='sorting'):
    items = Horizont[Label("Sort by:"), SortingComboBox(), AscendingButton()]
    to_connect: dict[str, list[str]] = {
        "sort_handler": ["sort_box.currentTextChanged"],
        "ascending_handler": ["ascending_btn.clicked"],
    }

    def __init__(self, dataview, *args, **kwargs):
        self.dataview = dataview
        super().__init__(*args, **kwargs)

    def update(self):
        fields = set(self.dataview.dataset.get_sort_fields())
        exists = set(self.sort_box.get_all_items())
        exists.remove(self.sort_box.lineEdit().placeholderText())
        if fields != exists:
            self.sort_box.set_items(fields)

    def ascending_handler(self, sender, *args):
        dataset = self.dataview.dataset
        value = not dataset.state.ascending
        dataset.set_ascending(value)
        sender.set_image(svg.ascending if value else svg.descending)

    def sort_handler(self, sender, text):
        value = text if sender.empty_state != text else None
        self.dataview.dataset.set_sort_key(value)
