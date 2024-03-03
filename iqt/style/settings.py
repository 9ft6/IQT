class Colors:
    none = 'rgba(0, 0, 0, 0)'
    drop_area = 'rgba(0, 0, 0, 0.5)'
    drop_area_border = 'rgba(0, 0, 0, 0.3)'
    progressbar_bg = 'rgba(255, 255, 255, 0.3)'
    drop_area_bg = 'rgba(0, 0, 0, 0.7)'
    white = 'rgba(255, 255, 255, 1)'
    green = 'rgba(52, 204, 103, 1)'
    blue = 'rgba(52, 103, 204, 1)'
    item_bg = 'rgba(47, 48, 50, 1)'
    lightest = 'rgba(86, 88, 90, 1)'
    asset_bg = 'rgba(34, 36, 38, 1)'  #222426
    block_bg = 'rgba(74, 75, 76, 1)'
    popup_bg = 'rgba(21, 22, 24, 1)'
    console_bg = 'rgba(17, 17, 17, 1)'
    start_screen_bg = 'rgba(21, 22, 24, 0.75)'
    tab_bar_selected = 'rgba(56, 58, 60, 1)' #383A3C
    error = 'rgba(204,103, 52, 1)'  #CC6734
    red = 'rgba(255, 22, 92, 1)'  #FF165C
    logo_color1 = 'rgba(32, 232, 246, 1)'  #20E8F6
    logo_color2 = 'rgba(103, 93, 197, 1)'  #675DC5
    purple = 'rgba(91, 83, 255, 1)'
    purple_opacity = 'rgba(91, 83, 255, 0.5)'
    slider_bg = 'rgba(174, 175, 176, 1)'
    selection_bg = 'rgba(120, 160, 230, 1)'
    footer_border = 'rgba(49, 51, 53, 1)'  #313335
    footer_bg = 'rgba(42, 43, 45, 1)'  #2A2B2D
    search_bg = 'rgba(127, 127, 127, 100)'
    asset_edit_bg = 'rgba(28, 29, 32, 1);'  #1c1d20


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
