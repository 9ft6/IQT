from iqt.app import Application
from iqt.window import Window
from iqt.components.widgets import Widget, Input, CheckBox
from iqt.components.layouts import Horizont, Vertical
from iqt.components import Button, Label, Image


class LoginWidget(
    Widget,
    name="main_widget",
    margins=(16, 8, 16, 8),
):
    items = Vertical[
        Horizont[..., Image("logo.png", fixed_width=160)],
        Horizont[Label("Please Login:")],
        Horizont[Label("login:"), ..., Input("login", fixed_width=160)],
        Horizont[Label("pass:"), ..., Input("password", fixed_width=160)],
        Horizont[CheckBox("Remember me"), ..., Button("login")],
    ]

    def items_handler(self, sender: Widget, *args, **kwargs):
        match sender.name:
            case "button":
                print("do login")
            case "checkbox":
                print("change config state")


class LoginWindow(
    Window,
    name="login_window",
    fixed_size=(280, 360),
    transparent=False,
    title="Please login",
    widget_model=LoginWidget,
):
    ...


class TestGUI(Application, start_window=LoginWindow):
    ...


if __name__ == '__main__':
    TestGUI().run()
