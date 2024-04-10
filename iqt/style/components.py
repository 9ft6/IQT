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
        background: {Colors.none};
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
    CurrentPageInput,
    PageQButton {{
        background: {Colors.gray};
        border: none;
        border-radius: 12px;
        width: 24px;
        height: 24px;
    }}
    CurrentPageInput {{
        background: {Colors.light};
    }}
    QWidget#scroll_area_widget {{
        background-color: {Colors.none};
    }}
    DataViewScrollArea {{
        background-color: {Colors.lightest};
    }}
'''

