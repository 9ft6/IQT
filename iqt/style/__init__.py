from .main import main
from . import components
from .settings import Colors, Fonts


base_style = '\n'.join([
    main,
    components.style,
])
