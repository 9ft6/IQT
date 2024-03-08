from iqt.app import Application
from iqt.window import Window
from iqt.components.widgets import Widget, Input, CheckBox
from iqt.components.layouts import Horizont, Vertical
from iqt.components import Button, Label, Image


class LoginWidget(
    Widget,
    name="main_widget",
):
    items = Vertical[
        ...,
        Horizont[..., Image("logo.png", fixed_height=60)],
        Horizont[Label("Please Login:")],
        Horizont[Label("login:"), ..., Input("login", fixed_width=160)],
        Horizont[Label("pass:"), ..., Input("password", fixed_width=160)],
        Horizont[Button("login"), ..., CheckBox("Remember me")],
        ...,
    ]

    def items_handler(self, sender: Widget, *args, **kwargs):
        match sender.name:
            case "button":
                print("do login")
            case "checkbox":
                print("change config state")


class LoginWindow(
    Window,
    fixed_size=(260, 260),
    transparent=False,
    title="Please login",
    widget_model=LoginWidget,
):
    ...


class TestGUI(Application, window_model=LoginWindow):
    ...


if __name__ == '__main__':
    TestGUI().run()
