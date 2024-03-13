from iqt.style.settings import Colors, Fonts


style = f'''
    QLabel#title {{
        {Fonts.title}
    }}
    .BaseImageButton {{
        background: {Colors.none};
        border: none;
    }}
    .SortingQWidget {{
        background-color: {Colors.red};
    }}
    PageQButton {{
        background: {Colors.gray};
        border: none;
        border-radius: 12px;
        width: 24px;
        height: 24px;
    }}
    PageQButton[active = true] {{
        background: {Colors.light};
    }}
    QWidget#scroll_area_widget,
    DataViewScrollArea {{
        background-color: {Colors.lightest};
    }}
'''

