from typing import Literal, Any

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from iqt.components.base import BaseObject, BaseConfig, BaseConfigResponse
from iqt.components.data_view.scroll_area import DataViewScrollArea


class DataViewConfig(BaseConfig):
        name: str = "data_view"
        direction: Literal["vertical", "horizont", "flow"]
        set_resizable: bool = True
        h_scroll_policy: Any = Qt.ScrollBarAlwaysOff
        v_scroll_policy: Any = Qt.ScrollBarAsNeeded
        scroll_bar_setter: str = "setVerticalScrollBar"


class BaseDataView(BaseObject):
    class Config(DataViewConfig):
        ...

    factory: QWidget = DataViewScrollArea

    def __init__(self, name=None, *args, **kwargs):
        kwargs["name"] = name
        super().__init__(*args, **kwargs)

    def add(self, widget: BaseObject | list[BaseObject]):
        widgets = widget if isinstance(widget, list) else [widget]
        for widget in widgets:
            self.widget.add_widget(widget)

    def remove(self, num: int):
        ...

    def clear(self):
        ...

    def post_init(self) -> None:
        copy_methods = ["add", "remove", "clear"]
        for m in copy_methods:
            if v := getattr(self, m, None):
                setattr(self.widget, m, v)
        self.widget.setup_layout(self.cfg)

    def init_widget(self, parent=None):
        return self.factory(parent)

    def config(self):
        return BaseConfigResponse(
            to_connect=self.to_connect,
            signals=self.signals,
            entity=self,
            widget_settings=self.build_config().get_settings(),
            widget=self.factory,
        )


class FlowDataView(BaseDataView):
    class Config(DataViewConfig):
        direction: Literal["vertical", "horizont", "flow"] = "flow"


class VerticalDataView(BaseDataView):
    class Config(DataViewConfig):
        direction: Literal["vertical", "horizont", "flow"] = "vertical"


class HorizontDataView(BaseDataView):
    class Config(DataViewConfig):
        direction: Literal["vertical", "horizont", "flow"] = "horizont"
        h_scroll_policy: Any = Qt.ScrollBarAsNeeded
        v_scroll_policy: Any = Qt.ScrollBarAlwaysOff
