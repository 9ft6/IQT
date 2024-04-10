from PySide6.QtWidgets import QPushButton, QLineEdit
from PySide6.QtGui import QIntValidator

from iqt.components.base import BaseConfig
from iqt.components.buttons import Button
from iqt.components.widgets import Widget, Input
from iqt.components.layouts import Horizont


class CurrentPageInput(QLineEdit):
    def set(self, page):
        self.setPlaceholderText(str(page))
        self.setText(str(page))


class CurrentPage(Input):
    factory = CurrentPageInput
    to_connect: dict = {
        "text_handler": ["textChanged"],
        "main_handler": ["editingFinished"],
    }

    def __init__(self, page: str, *args, root=None, **kwargs):
        self.page = page
        self.dataset = root.dataview.dataset
        super().__init__("current", *args, fixed_width=24, **kwargs)

    def post_init(self):
        self.widget.setPlaceholderText(str(self.page))
        validator = QIntValidator()
        validator.setRange(1, self.dataset.pages_count())
        self.widget.setValidator(validator)


class PageQButton(QPushButton):
    ...


class PageButton(Button):
    factory: Widget = PageQButton


class PaginationConfig(BaseConfig):
    name: str = 'pagination'


class Pagination(Widget):
    Config = PaginationConfig
    items = Horizont[None]

    def __init__(self, dataview, *args, **kwargs):
        self.dataview = dataview
        super().__init__(*args, **kwargs)

    def update(self):
        self.dataset = self.dataview.dataset
        pages = self.create_pages()
        self.widget.clear()
        self.widget.layout().addStretch()
        [self.add_button(p) for p in pages]
        self.widget.layout().addStretch()

    def main_handler(self, sender, *args, **kwargs):
        if int(sender.text()) != self.dataset.state.page:
            self.dataset.set_page(int(sender.text()))

    def text_handler(self, sender, value, *args, **kwargs):
        if value and int(value) not in self.dataset.pages():
            sender.set(self.dataset.state.page)

    def items_handler(self, sender, *args):
        if int(sender.text()) != self.dataset.state.page:
            self.dataset.set_page(int(sender.text()))

    def add_button(self, num: int):
        if isinstance(num, int):
            is_current = num == self.dataset.state.page
            widget = CurrentPage if is_current else PageButton
            widget = widget(str(num), root=self)
            self.widget.add_widget(widget)
        else:
            self.widget.layout().addStretch()

    def get_pages(self):
        dataset = self.dataset
        current = dataset.state.page

        # Getting all pages
        pages = dataset.pages()
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
