from iqt.style.settings import Colors, Fonts


style = f'''
    QWidget#strain_card {{
        background: {Colors.red};
        border: 1px solid green;
    }}
    QWidget#sorting {{
        background: {Colors.red};
        border: 1px solid green;
    }}
    QLabel#title {{
        {Fonts.title}
    }}
    .BaseImageButton {{
        background: {Colors.none};
        border: none;
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

