from typing import Literal

from iqt.components.base import BaseObject
from iqt.components.widgets import CustomQWidget, Widget
from iqt.components.layouts import HorizontNM, VerticalNM
from iqt.components.buttons import ImageButton
from iqt.components.animation import (
    AnimatedWidgetMixin,
    BaseAnimation,
    ResizeAnimation
)
from iqt.images import svg


SideBarDirection = Literal['top', 'bottom', 'left', 'right']


class SidebarWidget(CustomQWidget):
# class SidebarWidget(CustomQWidget, AnimatedWidgetMixin):
    # animations: list[BaseAnimation] = [ResizeAnimation]

    def expand(self, value: bool):
        print("expand", value)
        value = 150 if value else 15
        self.resize(value, self.height())


class Sidebar(Widget):
    class Config(Widget.Config):
        event_filter: bool = True
        animated: bool = True

    factory = SidebarWidget
    direction: SideBarDirection = "right"
    is_expanded: bool = False
    items: BaseObject = ...


    def generate_items(self):
        layout = HorizontNM if self.direction in ['left', 'right'] else VerticalNM
        return layout[ImageButton(getattr(svg, f"sidebar_btn_{self.direction}"))]

    def items_handler(self, sender, *args, **kwargs):
        self.is_expanded = not self.is_expanded
        self.widget.expand(self.is_expanded)
        print(sender, self.is_expanded)

