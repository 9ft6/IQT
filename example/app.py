from iqt.app import Application
from iqt.window import Window
from iqt.components.widgets import Widget, BaseInput as Input, BaseCheckBox as CheckBox
from iqt.components.layouts import Horizont, Vertical
from iqt.components import Label, Button


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
            case "button":
                ...  # do login
            case "checkbox":
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