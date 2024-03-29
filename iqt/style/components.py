from iqt.style.settings import Colors, Fonts, Scheme


style = f'''
    QWidget#pagination,
    QWidget#default_widget {{
        background: {Colors.none};
    }}
    PreviewLabel,
    QWidget#filter,
    QWidget#sorting {{
        background: {Scheme.frame};
        border-radius: 8px;
    }}
    QLabel#title {{
        {Fonts.title}
    }}
    .DynamicItemWidget {{
        border-radius: 8px;
        border: 1px solid {Scheme.main_bg};
    }}
    .BaseImageButton {{
        background: {Colors.none};
        border: none;
    }}
    PageQButton {{
        background: {Scheme.unit};
        border: none;
        border-radius: 12px;
        width: 24px;
        height: 24px;
    }}
    PageQButton[active = true] {{
        background: {Scheme.unit_active};
        border: {Scheme.unit_active_border};
    }}
    QWidget#scroll_area_widget {{
        background-color: {Colors.none};
    }}
    DataViewScrollArea {{
        background-color: {Scheme.frame};
    }}
'''

