from pathlib import Path

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import QRect

# QT native methods
native_methods = {
    "fixed_height": "setFixedHeight",
    "fixed_size": "setFixedSize",
    "min_size": "setMinimalSize",
    "fixed_width": "setFixedWidth",
    "margins": "setContentsMargins",
    "name": "setObjectName",
    "size": "resize",
    "spacing": "setSpacing",
    "style": "setStyleSheet",
    "text": "setText",
    "title": "setTitle",
    "set_resizable": "setWidgetResizable",
    "h_scroll_policy": "setHorizontalScrollBarPolicy",
    "v_scroll_policy": "setVerticalScrollBarPolicy",
    "hidden": "setHidden",
    "shortcut": "setShortcut"
}
# custom methods
custom_methods = {
    "image": "set_image",
    "items": "set_items",
    "empty_state": "set_empty_state",
    "value": "set_text",
}


def method_by_setting(object, setting):
    methods = {**native_methods, **custom_methods}
    if method_name := methods.get(setting):
        return getattr(object, method_name, None)
    else:
        return getattr(object, setting, None)


def setup_settings(object: QWidget, cfg):
    for setting, value in cfg.items():
        setup_setting(object, setting, value)


def setup_setting(object: QWidget, setting, value):
    # print(object, setting, value)
    method = method_by_setting(object, setting)
    if not method:
        return

    match setting:
        case "name":
            method(value)
            object.name = value
        case _:
            if isinstance(value, tuple):
                method(*value)
            else:
                method(value)


def setup_fonts(root):
    try:
        fonts_dir = Path(root.cfg.font_path)
        for font_file in fonts_dir.iterdir():
            if font_file.is_file() and font_file.suffix in ['.otf']:
                font_path = str(Path(font_file).absolute())
                font = QFontDatabase.addApplicationFont(font_path)
        font = QFont('Ubuntu Mono')
        font.setStyleStrategy(QFont.PreferAntialias)
        root.setFont(font)
    except Exception as e:
        print(f"Could not load fonts {e}")


def get_attr_recursive(obj, method_name, with_parent=False):
    if "." in method_name:
        parent_name, method_name = method_name.split(".", 1)
        if parent := get_attr_recursive(obj, parent_name):
            return get_attr_recursive(parent, method_name, with_parent=with_parent)
    else:
        if with_parent:
            return getattr(obj, method_name, None), obj
        else:
            return getattr(obj, method_name, None)


def get_widget_center_geometry(size):
    screen = QApplication.primaryScreen().geometry().center()
    center = screen
    x, y, (w, h) = center.x(), center.y(), size
    return QRect(x - w / 2, y - h / 2, *size)