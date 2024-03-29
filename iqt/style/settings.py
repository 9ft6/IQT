class Colors:
    # base
    none = 'rgba(0, 0, 0, 0)'
    green = 'rgba(52, 204, 103, 1)'
    blue = 'rgba(52, 103, 204, 1)'
    red = 'rgba(255, 21, 93, 1)'

    # grayscale
    white = 'rgba(255, 255, 255, 1)'
    lightest = 'rgba(85, 87, 89, 1)'
    light = 'rgba(72, 74, 76, 1)'
    light_gray = 'rgba(62, 64, 66, 1)'
    gray = 'rgba(43, 44, 46, 1)'
    dark_gray = 'rgba(31, 42, 53, 1)'
    dark = 'rgba(21, 22, 23, 1)'
    black = 'rgba(0, 0, 0, 1)'

    # special
    selection = 'rgba(120, 150, 225, 1)'


class Cs:
    dark_bg = 'rgba(23, 20, 20, 1)'
    light_bg = 'rgba(43, 40, 40, 1)'
    dirty_green = 'rgba(39, 54, 39, 1)'
    yellow = 'rgba(138, 101, 51, 1)'
    red = 'rgba(207, 106, 76, 1)'

class Scheme:
    main_bg = Cs.dark_bg
    frame = Cs.light_bg

    unit = Cs.yellow
    unit_border = f'1px solid {Cs.dirty_green}'

    unit_pressed = Cs.yellow
    unit_pressed_border = f'1px solid {Cs.red}'

    unit_hover = Cs.dark_bg
    unit_hover_border = f'1px solid {Cs.yellow}'

    unit_active = ''
    unit_active_border = f'1px solid {Cs.dirty_green}'


base_font = f'''
    font-family: Ubuntu Mono;
    font-style: normal;
    font-weight: 500;
    color: {Colors.white};
'''


class Fonts:
    normal = f'''
        {base_font}
        font-size: 14px;
    '''
    activated = f'''
        {base_font}
        font-size: 14px;
        color: {Scheme.main_bg};
    '''
    bold = f'''
        {base_font}
        font-size: 14px;
    '''
    normal_hover = f'''
        {base_font}
        font-size: 14px;
    '''
    small = f'''
        {base_font}
        font-size: 11px;
    '''
    title = f'''
        {base_font}
        font-style: bold;
        font-weight: bold;
        font-size: 16px;
    '''
