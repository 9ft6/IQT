from .settings import Colors, Fonts


main = f'''
    QMainWindow,
    QWidget {{
        background-color: {Colors.dark};
        border-radius: 0px;
        selection-background-color: {Colors.selection};
    }}
    QPushButton,
    QLabel {{
        {Fonts.normal}
        background: {Colors.none};
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
'''
