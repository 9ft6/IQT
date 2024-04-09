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
        pages = self.create_pages()
        self.widget.clear()
        self.widgets.clear()
        self.widget.layout().addStretch()
        [self.add_button(p) for p in pages]
        self.widget.layout().addStretch()
        self.ensure_current()

    def ensure_current(self, page=None):
        page = page or self.widget.dataset.state.page
        for n, w in self.widgets.items():
            w.set_active(str(n) == page)

        if page in self.widgets:
            self.widgets[page].set_active(True)

    def items_handler(self, sender, *args):
        page = int(sender.text())
        self.widget.dataset.set_page(page)
        self.ensure_current()

    def add_button(self, num: int):
        if isinstance(num, int):
            widget = PageButton(str(num))
            self.widgets[num] = widget
            self.widget.add_widget(widget)
        else:
            self.widget.layout().addStretch()

    def get_pages(self):
        dataset = self.widget.dataset
        current = dataset.state.page

        # Getting all pages
        pages_count = dataset.count() // dataset.per_page
        tail = dataset.count() % dataset.per_page
        pages = [x + 1 for x in range(0, pages_count + bool(tail))]

        # Splitting by current page
        current_index = pages.index(current) if current in pages else 1
        left = pages[:current_index]
        right = pages[current_index + 1:]

        # Take 2 before and after current page
        if len(left) > 2:
            left = reversed([pages[0], ...] + left[-2:])
        if len(right) > 2:
            right = right[:2] + [..., pages[-1]]
        return left, current, right

    def create_pages(self):
        left, current, right = self.get_pages()
        result = [current]
        for side in [left, right]:
            for page in side:
                if side == right:
                    result.append(page)
                else:
                    result.insert(0, page)
        return result
