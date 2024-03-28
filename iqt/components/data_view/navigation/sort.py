from pathlib import Path

from iqt.components import Widget, ComboBox, ImageButton, Label
from iqt.components.layouts import Horizont
from iqt.components.combo import ComboBoxConfig
from iqt.components.buttons import ButtonConfig
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
        fixed_size: tuple[int, int] = (24, 24)


class SortingWidget(Widget, name='sorting'):
    items = Horizont[Label("Sort by:"), SortingComboBox(), AscendingButton()]
    to_connect: dict[str, list[str]] = {
        "sort_handler": ["sort_box.currentTextChanged"],
        "ascending_handler": ["ascending_btn.clicked"],
    }

    def update(self):
        fields = set(self.widget.dataset.get_sort_fields())
        exists = set(self.sort_box.get_all_items())
        exists.remove(self.sort_box.lineEdit().placeholderText())
        if fields != exists:
            self.sort_box.set_items(fields)

    def ascending_handler(self, sender, *args):
        dataset = self.widget.dataset
        value = not dataset.state.ascending
        dataset.set_ascending(value)
        sender.set_image(svg.ascending if value else svg.descending)

    def sort_handler(self, sender, text):
        value = text if sender.empty_state != text else None
        self.widget.dataset.set_sort_key(value)
