from iqt.style.settings import Colors, Fonts


style = f'''
    QWidget#strain_card {{
        background: {Colors.gray};
        border: 1px solid green;
    }}
    QWidget#pagination,
    QWidget#default_widget {{
        background: {Colors.none};
    }}
    PreviewLabel,
    QWidget#filter,
    QWidget#sorting {{
        background: {Colors.light};
        border-radius: 8px;
    }}
    QLabel#title {{
        {Fonts.title}
    }}
    .DynamicItemWidget {{
        border-radius: 8px;
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

