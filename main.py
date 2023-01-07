import kivy.uix.button
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database
import re

db_functions = Database()
current_name = ""
current_password = ""


class CreateWindow(Screen):
    create_name = ObjectProperty(None)
    create_password = ObjectProperty(None)

    def submit_info(self):
        name, password = self.create_name.text, self.create_password.text
        if name != "" and len(name) >= 3:
            if password != "" and password_validator(password):
                result = db_functions.add_user(name, password)
                if result:
                    show_popup("Congratulations",
                               "The account has been created.\nYou can now login")
                    self.login_transition()
                    self.create_name.text = ""
                    self.create_password.text = ""
                else:
                    show_popup("Error",
                               "This username already exists")
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
    login_name = ObjectProperty(None)
    login_password = ObjectProperty(None)

    def submit_info(self):
        name, password = self.login_name.text, self.login_password
        if name != "" and password != "":
            result_for_the_given_name = list(db_functions.get_user_data(name))
            if result_for_the_given_name:
                if password.text == result_for_the_given_name[0][2]:
                    m.current = "main"
                    self.login_name.text = ""
                    self.login_password.text = ""
                    global current_name, current_password
                    current_id, current_name = result_for_the_given_name[0][:2]
                else:
                    show_popup("Error",
                               "Incorrect password")
            else:
                show_popup("Error",
                           "Incorrect name")

    def create_transition(self):
        m.current = "create"


class AddNote(Screen):
    title = ObjectProperty(None)
    text = ObjectProperty(None)

    def add_note_to_database(self):
        pass

    def add_note(self):
        self.manager.get_screen('main').ids.scroll.add_widget(Button(text="test"))

    def main_transition(self):
        m.current = "main"


class MainWindow(Screen):

    def add_note_transition(self):
        m.current = "add_note"

    def logout(self):
        m.current = "login"

    def delete_account(self):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Are you sure you want to delete this account?\nThis action is permanent!!!"))

        popup = Popup(title='Confirmation', title_size=(30),
                      title_align='center', content=content,
                      size_hint=(None, None), size=(400, 400))
        content.add_widget(Button(text="yes"))
        content.add_widget(Button(text="no", on_release=popup.dismiss))
        popup.open()


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

screens = [LoginWindow(name="login"), CreateWindow(name="create"), MainWindow(name="main"), AddNote(name="add_note")]
[m.add_widget(screen) for screen in screens]

# m.current = "main"


class MyMainApp(App):
    def build(self):
        Window.clearcolor = (0.5, 0.7, 0.8, 1)
        db_functions.create_tables()
        return m


if __name__ == "__main__":
    MyMainApp().run()
