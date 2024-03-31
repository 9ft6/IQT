from PySide6.QtWidgets import QPushButton

from iqt.components.base import BaseConfig
from iqt.components.buttons import Button
from iqt.components.widgets import Widget
from iqt.components.layouts import Horizont


class PageQButton(QPushButton):
    ...


class PageButton(Button):
    factory: Widget = PageQButton

    def set_active(self, active: bool):
        self.widget.setProperty("active", active)
        self.widget.setStyle(self.widget.style())


class PaginationConfig(BaseConfig):
    name: str = 'pagination'


class Pagination(Widget):
    Config = PaginationConfig
    items = Horizont[None]

    def pre_init(self):
        self.widgets = {}

    def update(self):
        dataset = self.widget.dataset
        pages = range(1, int(dataset.count() / dataset.per_page) + 1)
        pages = list(pages) or [1]
        self.widget.clear()
        self.widgets.clear()
        [self.add_button(p) for p in pages]
        self.ensure_current()

    def ensure_current(self, page=None):
        page = page or self.widget.dataset.state.page
        for n, w in self.widgets.items():
            w.set_active(str(n) == page)

        self.widgets[page].set_active(True)

    def items_handler(self, sender, *args):
        page = int(sender.text())
        self.widget.dataset.set_page(page)
        self.ensure_current(page)

    def add_button(self, num: int):
        widget = PageButton(str(num))
        self.widgets[num] = widget
        self.widget.add_widget(widget)
