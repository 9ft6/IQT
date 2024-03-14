from pathlib import Path

from iqt.components.widgets import CustomQWidget
from iqt.components import Widget, ComboBox, Button, Label
from iqt.components.layouts import Horizont
from iqt.components.combo import ComboBoxConfig
from iqt.components.buttons import ButtonConfig
from iqt.images import svg



class FilterWidget(Widget, name='filter'):
    margins: tuple[int, int, int, int] = (0, 0, 0, 0)
    items = Horizont[Label("Filter:"), Button("querying")]
    to_connect: dict[str, list[str]] = {
        "sort_handler": ["sort_box.currentTextChanged"],
        "ascending_handler": ["ascending_btn.clicked"],
    }
