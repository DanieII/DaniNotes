import kivy.uix.button
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import Database
from hashlib import sha256
import re

db_functions = Database()
current_id = ""
current_name = ""


class CreateWindow(Screen):
    create_name = ObjectProperty(None)
    create_password = ObjectProperty(None)

    def submit_info(self):
        name, password = self.create_name.text, self.create_password.text
        if name != "" and len(name) >= 3:
            if password != "" and password_validator(password):
                password_after_hashing = get_hashed(password)
                result = db_functions.add_user(name, password_after_hashing)
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
        name, password = self.login_name.text, self.login_password.text
        if name != "" and password != "":
            result_for_the_given_name = list(db_functions.get_user_data(name))
            if result_for_the_given_name:
                password_after_hashing = get_hashed(password)
                if password_after_hashing == result_for_the_given_name[0][2]:
                    m.current = "main"
                    self.login_name.text, self.login_password.text = "", ""
                    global current_id, current_name
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
        title, text = self.title.text, self.text.text
        if title != "" and text != "":
            db_functions.add_note(current_id, title, text)
            self.title.text, self.text.text = "", ""
        else:
            show_popup("Error",
                       "Make sure to fill every text field")

    def main_transition(self):
        m.current = "main"


already_loaded_notes_ids = list()


class MainWindow(Screen):

    def show_notes(self):
        remove_widgets()
        self.all_user_notes = list(db_functions.get_user_notes(current_id))
        if self.all_user_notes:
            for index in range(len(self.all_user_notes)):
                title = self.all_user_notes[index][2]
                note_id = self.all_user_notes[index][0]
                text = self.all_user_notes[index][3]
                if note_id not in already_loaded_notes_ids:
                    button = Button(text=title,
                                    on_release=lambda x: self.see_and_edit_note(title, note_id, text),
                                    background_color=[0.8, 1, 1, 1])
                    self.ids.scroll.add_widget(button)
                    already_loaded_notes_ids.append(note_id)
                    self.ids[index] = button
        else:
            show_popup("Error",
                       "No notes to show")

    def see_and_edit_note(self, title, note_id, text):
        content = BoxLayout(orientation="vertical")
        new_text = TextInput(text=text)
        content.add_widget(new_text)
        popup = Popup(title=title, title_size=30,
                      title_align='center', content=content,
                      size_hint=(None, None), size=(550, 550))
        content.add_widget(
            Button(text="Save changes",
                   on_press=lambda x: db_functions.edit_note(note_id, new_text.text),
                   on_release=popup.dismiss))
        content.add_widget(
            Button(text="Delete", on_release=lambda x: delete_note(popup, note_id)))
        content.add_widget(Button(text="Go back", on_release=popup.dismiss))
        popup.open()

    def add_note_transition(self):
        m.current = "add_note"

    def logout(self):
        m.current = "login"
        remove_widgets()

    def delete_account_popup(self):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text="Are you sure you want to delete this account?\nThis action is permanent!!!"))
        popup = Popup(title='Confirmation', title_size=30,
                      title_align='center', content=content,
                      size_hint=(None, None), size=(600, 500))
        content.add_widget(Button(text="yes", on_release=lambda x: delete_account(popup)))
        content.add_widget(Button(text="no", on_release=popup.dismiss))
        popup.open()
        remove_widgets()


def delete_account(popup):
    popup.dismiss()
    db_functions.delete_user(current_id)
    m.transition.direction = "up"
    m.current = "login"


def delete_note(popup, noteid):
    popup.dismiss()
    db_functions.delete_note(noteid)
    already_loaded_notes_ids.clear()


def remove_widgets():
    already_loaded_notes_ids.clear()
    for child in m.get_screen("main").children[0].children[2].children[0].children[0].children[:]:
        m.get_screen("main").children[0].children[2].children[0].children[0].remove_widget(child)


def show_popup(title, content):
    popup = Popup(title=title, content=Label(text=content), title_size=30,
                  title_align='center', size_hint=(None, None), size=(450, 450))
    popup.open()


def password_validator(passwd):
    pattern = "(?=^.{5,}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])"
    result = re.match(pattern, passwd)
    if result:
        return True
    return False


def get_hashed(password):
    hash = sha256(password.encode())
    return str(hash.hexdigest())


class Manager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")
m = Manager()

screens = [LoginWindow(name="login"), CreateWindow(name="create"), MainWindow(name="main"), AddNote(name="add_note")]
[m.add_widget(screen) for screen in screens]


class MyMainApp(App):
    def build(self):
        Window.clearcolor = (0.5, 0.7, 0.8, 1)
        db_functions.create_tables()
        return m


if __name__ == "__main__":
    MyMainApp().run()
