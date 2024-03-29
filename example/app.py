try:
    import iqt
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path().resolve() / ".."))

from iqt.app import Application
from iqt.window import Window
from iqt.components.widgets import Widget, Input
from iqt.components.layouts import Horizont, Vertical
from iqt.components import Label, Title, Image, CheckBox, Submit
from iqt.components.data_view.dynamic import DynamicDataView
from dataset import Supply, Supplies


class View(DynamicDataView, size=(1600, 1024)):
    item_model = Supply()
    dataset = Supplies


class LoginInvalidWidget(Widget, size=(240, 80), margins=(16, ) * 4):
    items = Vertical[Label("login is biba or boba"), Submit("try again")]
    to_connect = {"back_to_login": ["submit.clicked"]}

    def back_to_login(self, *args, **kwargs):
        self.window.change_widget(LoginWidget())


class LoginWidget(Widget, size=(280, 360), margins=(16, ) * 4):
    items = Vertical[
        Horizont[..., Image("logo.png", fixed_width=160)],
        Horizont[Title("Please Login:")],
        Horizont[Label("login:"), ..., Input("login", fixed_size=(160, 32))],
        Horizont[Label("pass:"), ..., Input("pwd", fixed_size=(160, 32))],
        Horizont[CheckBox(text="Remember me"), ..., Submit("login")],
    ]

    def items_handler(self, sender: Widget, *args, **kwargs):
        match sender.name:
            case "submit":
                if self.login.text() in ["biba", "boba"]:
                    self.window.change_widget(View(size=(1600, 1024)))
                else:
                    self.window.change_widget(LoginInvalidWidget())
            case "checkbox":
                print("change config state")


class TestGUI(Application):
    class StartWindow(Window, title="Please login", widget_model=LoginWidget):
        ...


if __name__ == '__main__':
    TestGUI().run()
