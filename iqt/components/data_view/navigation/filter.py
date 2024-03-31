from iqt.components.widgets import Widget
from iqt.components.buttons import Button
from iqt.components.labels import Label
from iqt.components.layouts import Horizont


class FilterWidget(Widget, name='filter'):
    margins: tuple[int, int, int, int] = (0, 0, 0, 0)
    items = Horizont[Label("Filter:"), Button("querying")]
    to_connect: dict[str, list[str]] = {
        "sort_handler": ["sort_box.currentTextChanged"],
        "ascending_handler": ["ascending_btn.clicked"],
    }
