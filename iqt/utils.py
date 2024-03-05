from pathlib import Path

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFontDatabase, QFont


def method_by_setting(object, setting):
    methods = {
        "fixed_height": "setFixedHeight",
        "fixed_size": "setFixedSize",
        "fixed_width": "setFixedWidth",
        "margins": "setContentsMargins",
        "name": "setObjectName",
        "size": "resize",
        "spacing": "setSpacing",
        "style": "setStyleSheet",
        "text": "setText",
    }
    if method_name := methods.get(setting):
        return getattr(object, method_name, None)


def setup_settings(object: QWidget, cfg):
    for setting, value in cfg.get_settings().items():
        if method := method_by_setting(object, setting):
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
