from typing import Any
from pathlib import Path

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPixmap, QPainter, QImage
from PySide6.QtCore import QUrl, QObject, QByteArray
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from pydantic import BaseModel, Field

from iqt.utils import setup_settings

Size: tuple[int, int] = ...


class ConfigurableType(type):
    def __new__(cls, _name, bases, namespace, **opts):
        namespace["_cfg_extra"] = opts or {}
        return super().__new__(cls, _name, bases, namespace)


class SignalModel(BaseModel):
    type: Any = object
    name: str
    method: str = None


class BaseConfig(BaseModel, arbitrary_types_allowed=True):
    name: str = "object"
    text: str = ""
    margins: tuple[int, int, int, int] = Field(None)
    to_connect: dict[str, list] = Field({})
    signals: list[SignalModel] = Field([])
    size: Size = Field(None)
    fixed_size: Size = Field(None)
    fixed_width: int = Field(None)
    hidden: bool = Field(False)
    shortcut: str = Field(None)

    def get_settings(self):
        result = self.model_dump(by_alias=True, exclude_none=True)
        result["signals"] = self.signals
        return result


class BaseConfigResponse(BaseModel, arbitrary_types_allowed=True):
    to_connect: dict[str, list] = Field({})
    signals: list[SignalModel] = Field([])
    entity: Any
    widget_settings: dict
    widget: Any


class LayoutConfigResponse(BaseConfigResponse, arbitrary_types_allowed=True):
    layout_settings: dict
    layout: Any
    items: list


class BaseObject(metaclass=ConfigurableType):
    class Config(BaseConfig):
        ...

    name: str = "object"
    cfg: Config
    widget: QWidget
    factory: QWidget
    to_connect: dict = {}
    signals: list[SignalModel] = []

    _cfg_extra: dict = None

    def __init__(self, *args, **kwargs):
        self.app = QApplication.instance()
        self._cfg_extra = {**self._cfg_extra, **kwargs}

    def build_config(self):
        self.cfg = self.Config(**(self._cfg_extra or {}))
        return self.cfg

    def config(self):
        return BaseConfigResponse(
            to_connect=self.to_connect,
            signals=self.signals,
            entity=self,
            widget_settings=self.build_config().get_settings(),
            widget=self.factory,
        )

    def pre_init(self):
        ...

    def post_init(self):
        ...

    def init_widget(self, parent=None):
        return self.factory(parent)

    def create_widget(self, parent=None):
        self.pre_init()
        self.widget = self.init_widget(parent)
        config = self.config()
        setup_settings(self.widget, config.widget_settings)
        self.post_init()
        return self.widget


class BaseImageWidgetMixin:
    net_manager: QNetworkAccessManager

    def load_from_web(self, image: str):
        self.net_manager = QNetworkAccessManager()
        self.net_manager.finished.connect(self.on_image_loaded)
        self.net_manager.get(QNetworkRequest(QUrl(image)))

    def on_image_loaded(self, reply):
        url = reply.request().url().toString()
        if 'svg' in reply.header(QNetworkRequest.ContentTypeHeader) or url.endswith('.svg'):
            self.set_svg(reply.readAll())

        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll())
        self.set_pixmap(pixmap)

    def set_image(self, image: str):
        if isinstance(image, str) and "<svg " in image:
            self.set_svg(image)
        elif Path(image).exists():
            self.set_pixmap(QPixmap(image))
        elif QUrl(image).isValid():
            self.load_from_web(image)

    def set_svg(self, svg: str):
        renderer = QSvgRenderer()
        renderer.load(QByteArray(svg.encode('utf-8')))
        image = QImage(renderer.defaultSize(), QImage.Format_ARGB32)
        image.fill(0)  # Transparent background

        painter = QPainter(image)
        renderer.render(painter)
        painter.end()

        self.set_pixmap(QPixmap.fromImage(image))

    def set_pixmap(self, pixmap: QPixmap):
        if pixmap:
            width, height = size = pixmap.size().toTuple()
            ratio = max(size) / min(size)

            if ratio > 16 / 9:
                if width > height:
                    new_width = height * 16 / 9
                    crop_x = (pixmap.width() - new_width) / 2
                    pixmap = pixmap.copy(crop_x, 0, new_width, pixmap.height())
                else:
                    new_height = width * 16 / 9
                    crop_y = (pixmap.height() - new_height) / 2
                    pixmap = pixmap.copy(0, crop_y, pixmap.width(), new_height)

            scaled = pixmap.scaledToWidth(self.width())
            self.setPixmap(scaled)
        else:
            from iqt.images import svg
            self.set_image(svg.no_preview)


class BaseWidget(BaseObject):
    factory: QObject
    items: Any
    window: Any
    layout_extra_settings: dict = None

    def config(self):
        widget_settings = self.build_config().get_settings()
        self.items = items = self.generate_items() or self.items
        layout_settings = items.build_config().get_settings()
        layout_settings.update(self.layout_extra_settings or {})
        return LayoutConfigResponse(
            to_connect=self.to_connect,
            signals=self.signals,
            entity=self,
            widget_settings=widget_settings,
            layout_settings=layout_settings,
            widget=self.factory,
            layout=self.items.factory,
            items=self.items.items,
        )

    def generate_items(self):
        ...
