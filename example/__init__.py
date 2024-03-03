from abc import abstractmethod

from iqt.app import Application, AppConfig
from iqt.window import Window, WindowConfig
from iqt.widgets.widgets import Widget, WidgetConfig
from iqt.widgets.base import Size, BaseObject
from iqt.widgets.layouts import BaseLayout
from example.widgets import Horizont, Vertical, Label, Input, Button, CheckBox


class LoginWidget(Widget):
    class Config(WidgetConfig):
        layout: BaseLayout = Vertical[
            ...,
            Horizont[Label("Please Login:")],
            Horizont[Label("login:"), Input("login")],
            Horizont[Label("pass:"), Input("password")],
            Horizont[Button("login"), ..., CheckBox("Remember me")],
            # Horizont[..., ],
            ...,
        ]
        name: str = "main_widget"

    @abstractmethod
    def items_handler(self, sender: Widget, *args, **kwargs):
        match sender.name:
            case "login_button":
                ...  # do login
            case "remember_me":
                ...  # change config state


class LoginWindow(Window):
    class Config(WindowConfig):
        widget_model: BaseObject = LoginWidget
        title: str = "Please login"
        fixed_size: Size = 480, 240
        transparent: bool = False


class LeaflyGUI(Application):
    class Config(AppConfig):
        window_model: Window = LoginWindow


if __name__ == '__main__':
    app = LeaflyGUI()
