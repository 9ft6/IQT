from pathlib import Path

from iqt.components.buttons import ImageButton, ButtonConfig
from iqt.components.widgets import Widget
from iqt.components.layouts import Horizont
from iqt.events import OpenFilter
from iqt.images import svg


class FilterButton(ImageButton):
    class Config(ButtonConfig):
        name: str = "filter_btn"
        image: str | Path = svg.filter
        fixed_size: tuple[int, int] = (20, 20)


class FilterWidget(Widget, name='filter'):
    margins: tuple[int, int, int, int] = (0, 0, 0, 0)
    items = Horizont[FilterButton()]

    def __init__(self, dataview, *args, **kwargs):
        self.dataview = dataview
        self.dataset = dataview.dataset
        super().__init__(*args, **kwargs)

    def items_handler(self, sender, *args, **kwargs):
        self.send_event(OpenFilter(str(id(self.dataview))))
