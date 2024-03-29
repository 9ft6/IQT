from .settings import Colors, Fonts


main = f'''
    QMainWindow,
    QWidget {{
        background-color: {Colors.dark};
        selection-background-color: {Colors.selection};
    }}
    QMainWindow > QWidget,
    QMainWindow > QWidget > QWidget {{
        border-radius: 16px;
    }} 
    QPushButton,
    QLabel {{
        {Fonts.normal}
        background: {Colors.none};
    }}
    QPushButton:hover {{
        background: {Colors.gray};
        border: 1px solid {Colors.white};
    }}
    QPushButton:clicked {{
        background: {Colors.light_gray};
        border: 1px solid {Colors.white};
    }}
    ButtonQWidget {{
        background: {Colors.light};
        border-radius: 4px;
        height: 24px;
        padding-left: 8px;
        padding-right: 8px;
    }}
    QLineEdit {{
        {Fonts.normal}
        color: {Colors.white};
        background: {Colors.gray};
        border-radius: 6px;
        line-height: 24px;
        padding-left: 4px;
        padding-right: 0px;
    }}
    QTextEdit {{
        {Fonts.normal}
        color: {Colors.white};
        background: {Colors.light};
        border-radius: 6px;
    }}
    QComboBox {{
        {Fonts.normal}
        background: {Colors.gray};
        border-radius: 6px;
        height: 24;
        font-size: 14px;
    }}
    QComboBox > QLineEdit {{
        {Fonts.normal}
        background: {Colors.none};
    }}
    QComboBox::drop-down {{
        {Fonts.normal}
        border-radius: 6px;
        border: 0px solid {Colors.none};
        height: 48px;
        background-color: {Colors.none};
        color: {Colors.white};
    }}
    QComboBox::down-arrow {{
        background-color: {Colors.none};
        image: url(images/arrow_down.png);
        width: 12px;
        height: 8px;
        bottom: 12px;
        right: 2px;
    }}
    QComboBox::down-arrow:on {{
        bottom: 9px;
    }}
    QTableWidget {{
        {Fonts.normal}
        background: {Colors.light};
        border-radius: 6px;
    }}
    QAbstractItemView {{
        {Fonts.normal}
        selection-background-color: {Colors.dark_gray};
        background-color: {Colors.gray};
        border: 0px solid {Colors.none};
    }}
    .QMenu {{
        color: {Colors.white};
        background: {Colors.light};
    }}
    .QMenu::item:selected {{
        color: {Colors.white};
        background: {Colors.gray};
    }}
    QDialog {{
        {Fonts.normal}
        background-color: {Colors.dark_gray};
        border-radius: 2px;
    }}
    .DialogBttn {{
        {Fonts.normal}
        height: 32px;
        background: {Colors.green};
        border-radius: 8px;
    }}
    .ToolTip > QLabel {{
        {Fonts.normal}
        background: {Colors.dark};
        color: {Colors.red};
        font-size: 12px;
        padding-left: 8px;
        padding-right: 8px;
        border-radius: 0px;
        border: 1px solid {Colors.red};
    }}
    QScrollArea {{
        border-radius: 4px;
    }}
    QScrollBar:vertical {{
        border: 0px;
        background: {Colors.lightest};
        width: 16px;
        margin: 0px 0px 0px 0px;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
    }}
    QScrollBar:horizontal {{
        border: 0px;
        background: {Colors.lightest};
        height: 12px;
        border-radius: 0px;
        margin: 0px 0px 0px 0px;
        border-bottom-left-radius: 4px;
        border-bottom-right-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {Colors.gray};
        min-height: 32px;
        width: 10px;
        border-radius: 5px;
        margin: 2px 2px 2px 2px;
    }}
    QScrollBar::handle:horizontal {{
        background: {Colors.gray};
        min-width: 32px;
        height: 10px;
        border-radius: 5px;
        margin: 0px 2px 2px 2px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::up-arrow:vertical,
    QScrollBar::down-arrow:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar:left-arrow:horizontal,
    QScrollBar::sub-page:horizontal, QScrollBar::add-page:horizontal, QScrollBar::right-arrow:horizontal {{
        background: {Colors.none};
    }}
    QWidget#popup {{
        background: rgba(0, 0, 0, 0.8);
    }}
    QWidget#title_bar {{
        background: rgba(0, 0, 0, 0.1);
    }}
    QWidget#title_bar[active = true] {{
        background: rgba(0, 0, 0, 0.8);
    }}
    QLabel#popup_resize_label {{
        background: rgba(0, 0, 0, 0.0);
        border-right: 2px solid {Colors.lightest};
        border-bottom: 2px solid {Colors.lightest};
    }}
'''
