
# IQT Framework

Welcome to the IQT Framework, a fresh way to make GUIs in Python. We know that using QT often means writing a lot of the same code over and over for each part of your app. It can get pretty overwhelming with all the settings you need to tweak. So we're building IQT to make things way easier.

With IQT, you can put together the visual parts of your app fast, with just a few lines of code. It lets you stay focused on what your app should do, not on the repetitive setup stuff. This means you get to the fun part of making your app work the way you want it to, quicker.

Keep an eye out for updates as we keep building and improving IQT.
## Simple example

Below is a sample code snippet to illustrate the simplicity of creating a login interface with IQT:

![Login Interface Preview](example/view.png)

```python
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

```
