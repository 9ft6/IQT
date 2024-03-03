from iqt.app import Application
from iqt.window import Window
from iqt.widgets.widgets import Widget
from example.widgets import Horizont, Vertical, Label, Input, Button, CheckBox


class LoginWidget(
    Widget,
    name="main_widget",
    layout=Vertical[
        ...,
        Horizont[Label("Please Login:")],
        Horizont[Label("login:"), Input("login")],
        Horizont[Label("pass:"), Input("password")],
        Horizont[Button("login"), ..., CheckBox("Remember me")],
        ...,
    ],
):
    def items_handler(self, sender: Widget, *args, **kwargs):
        match sender.name:
            case "login_button":
                ...  # do login
            case "remember_me":
                ...  # change config state


class LoginWindow(
    Window,
    fixed_size=(480, 240),
    transparent=False,
    title="Please login",
    widget_model=LoginWidget,
):
    ...


class TestGUI(Application, window_model=LoginWindow):
    ...


if __name__ == '__main__':
    TestGUI().run()
