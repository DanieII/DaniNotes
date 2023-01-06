from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database
import re

db_functions = Database()


class CreateWindow(Screen):
    create_name = ObjectProperty(None)
    create_password = ObjectProperty(None)

    def submit_info(self):
        name, password = self.create_name.text, self.create_password.text
        if name != "" and len(name) >= 3:
            if password != "" and password_validator(password):
                db_functions.add_user(name, password)
                show_popup("Congratulations",
                           "The account has been created.\nYou can now login")
                self.login_transition()
            else:
                show_popup("Error",
                           "Password Requirements:\n- 5 or more characters\n- at least 1 upper and lower letter\n- a"
                           " digit")
        else:
            show_popup("Error",
                       "The username must be at least 3 characters")

    def login_transition(self):
        m.current = "login"


class LoginWindow(Screen):
    name = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit_info(self):
        pass

    def create_transition(self):
        m.current = "create"


class MainWindow(Screen):
    pass


def show_popup(title, content):
    popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 400))
    popup.open()


def password_validator(passwd):
    # A valid string is a string containing at least 5 characters, 1 digit, 1 lowercase and 1 uppercase
    pattern = "(?=^.{5,}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])"
    result = re.match(pattern, passwd)
    if result:
        return True
    return False


class Manager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")
m = Manager()

screens = [LoginWindow(name="login"), CreateWindow(name="create"), MainWindow(name="main")]
[m.add_widget(screen) for screen in screens]


class MyMainApp(App):
    def build(self):
        Window.clearcolor = (0.6, 0.9, 0.7, 1)
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        db_functions.create_tables()
        return m


if __name__ == "__main__":
    MyMainApp().run()
