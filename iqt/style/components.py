from iqt.style.settings import Colors, Fonts


style = f'''
    QLabel#title {{
        {Fonts.title}
    }}
    .BaseImageButton {{
        background: {Colors.none};
        border: none;
    }}
    QWidget#scroll_area_widget,
    DataViewScrollArea {{
        background-color: {Colors.lightest};
    }}
'''

