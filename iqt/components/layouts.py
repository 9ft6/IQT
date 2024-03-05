from iqt.components.base import BaseWidgetObject
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout, QLayout
from PySide6.QtCore import Qt, QSize, QRect, QPoint


class BaseLayout(BaseWidgetObject):
    items: tuple

    def __init__(self, items, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = items

    @classmethod
    def __class_getitem__(cls, key):
        return cls(key if isinstance(key, tuple) else (key, ))

    def create_widget(self, parent=None) -> QWidget:
        return self.factory(parent, *self.cfg.init_args, **self.cfg.init_kwargs)

    def get_construct(self):
        return {
            "entity": self,
            "items": [
                i.get_construct() if isinstance(i, BaseLayout) else i
                for i in self.items
            ],
        }


class Horizont(BaseLayout, name="base_horizont"):
    factory: QBoxLayout = QHBoxLayout


class Vertical(BaseLayout, name="base_vertical"):
    factory: QBoxLayout = QVBoxLayout


class BaseFlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.root = parent
        self._item_list = []
        self.height = 0

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addStretch(self):
        ...

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if index >= 0 and index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.height
        return height

    def setGeometry(self, rect):
        super(BaseFlowLayout, self).setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        spacing = self.spacing() + 1

        for item in self._item_list:
            item_hint = item.sizeHint()

            if item.widget().isHidden():
                continue

            next_x = x + item_hint.width() + spacing
            if next_x - spacing > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spacing
                next_x = x + item_hint.width() + spacing
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item_hint))

            x = next_x
            line_height = max(line_height, item_hint.height())
        self.height = y + line_height - rect.y()
        return self.height


class Flow(BaseLayout):
    name: str = "base_flow"
    factory: QLayout = BaseFlowLayout
