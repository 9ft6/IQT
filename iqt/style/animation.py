from .settings import Colors, Fonts, Scheme


style = f'''
    QPushButton:hover {{
        {Fonts.activated}
        background: {Scheme.unit_active};
        border: 1px solid {Scheme.unit_hover};
    }}
    QPushButton:pressed {{
        {Fonts.activated}
        background: {Scheme.unit_pressed};
        border: 1px solid {Scheme.unit_active};
    }}
    
    
    
    QScrollBar::handle:horizontal:hover,
    QScrollBar::handle:vertical:hover {{
        background: {Scheme.unit_hover};
    }}
'''
