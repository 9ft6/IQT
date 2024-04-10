from iqt.components.widgets import Widget
from iqt.components.labels import Label
from iqt.components.layouts import Horizont


class FilterWidget(Widget, name='filter'):
    margins: tuple[int, int, int, int] = (0, 0, 0, 0)

    def __init__(self, dataview, *args, **kwargs):
        self.dataview = dataview
        self.dataset = dataview.dataset
        super().__init__(*args, **kwargs)

    def generate_items(self):
        model = self.dataview.dataset.item_model
        if model.filter_fields:
            fields = [Label(f) for f in model.filter_fields]
            items = [Label("Filter:"), *fields]
        else:
            items = [None]

        return Horizont[*items]
