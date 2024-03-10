from iqt.style.settings import Colors, Fonts


style = f'''
    QLabel#title {{
        {Fonts.title}
    }}
    QWidget#scroll_area_widget,
    DataViewWidget {{
        background-color: {Colors.lightest};
    }}
'''

