from .settings import Colors, Fonts


main = f'''
    QMainWindow,
    LogsWindow,
    .SoftwareSettingsWindow {{
        background-color: {Colors.asset_bg};
        border-radius: 0px;
        selection-background-color: {Colors.selection_bg};
    }}
    .QGraphicsView, .View {{
        background: {Colors.none};
        border: 0px;
    }}
    QPushButton,
    QLabel {{
        {Fonts.normal}
        background: {Colors.none};

    }}
    QLineEdit {{
        {Fonts.normal}
        color: {Colors.white};
        background: {Colors.item_bg};
        border-radius: 6px;
        line-height: 24px;
        padding-left: 4px;
        padding-right: 0px;
    }}
    QTextEdit {{
        {Fonts.normal}
        color: {Colors.white};
        background: {Colors.block_bg};
        border-radius: 6px;
    }}
    QSlider::handle:horizontal {{
        width: 12px;
        border-radius: 6px;
        background: {Colors.white};
    }}
    QSlider::add-page:horizontal {{
        border-radius: 3px;
        background: {Colors.block_bg};
    }}
    QSlider::sub-page:horizontal {{
        border-radius: 3px;
        background: {Colors.slider_bg};
    }}
    QComboBox {{
        {Fonts.normal}
        background: {Colors.item_bg};
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
    QCheckBox {{
        {Fonts.normal}
        spacing: 0;
        letter-spacing: 0.15px;
    }}
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border: 0px;
        background: {Colors.item_bg};
        border-radius: 4px;
        margin-right: 8px;
    }}
    QCheckBox::indicator:checked {{
       background: {Colors.purple};
       image: url("images/vector.png");
    }}
    QCheckBox::indicator:indeterminate {{
        background: {Colors.purple_opacity};
        image: url("images/semi_checked.png");
    }}
    QTableWidget {{
        {Fonts.normal}
        background: {Colors.block_bg};
        border-radius: 6px;
    }}
    QAbstractItemView {{
        {Fonts.normal}
        selection-background-color: {Colors.asset_bg};
        background-color: {Colors.item_bg};
        border: 0px solid {Colors.none};
    }}
    .QMenu {{
        color: {Colors.white};
        background: {Colors.block_bg};
    }}
    .QMenu::item:selected {{
        color: {Colors.white};
        background: {Colors.item_bg};
    }}
    QDialog {{
        {Fonts.normal}
        background-color: {Colors.asset_bg};
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
        background: {Colors.start_screen_bg};
        color: {Colors.red};
        font-size: 12px;
        padding-left: 8px;
        padding-right: 8px;
        border-radius: 0px;
        border: 1px solid {Colors.red};
    }}
'''
