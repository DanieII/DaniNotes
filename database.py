import sqlite3
import sqlite3 as sql


class Database:
    def __init__(self):
        self.connection = sql.connect("my_database.db")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE if not exists users (
                            userid INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT
                            )""")
        self.cursor.execute("""CREATE TABLE if not exists notes (
                            noteid INTEGER PRIMARY KEY AUTOINCREMENT ,
                            userid INTEGER,
                            note_title TEXT,
                            note_data TEXT
                            )""")
        self.connection.commit()

    def get_user_data(self, username):
        current_data = self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return current_data

    def get_user_notes(self, userid):
        current_notes = self.cursor.execute("SELECT * FROM notes WHERE userid=?", (userid,))
        return current_notes

    def add_note(self, userid, title, data):
        self.cursor.execute("""INSERT INTO notes(userid, note_title, note_data)
                                VALUES(?,?,?)""", (userid, title, data))
        self.connection.commit()

    def edit_note(self, note_id, new_text):
        self.cursor.execute("UPDATE notes SET note_data=? WHERE noteid=?", (new_text, note_id))
        self.connection.commit()

    def add_user(self, user, password):
        try:
            self.cursor.execute("""INSERT INTO users(username,password)
                                    VALUES(?,?)""", (user, password))
            self.connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def delete_user(self, userid):
        self.cursor.execute("DELETE FROM users WHERE userid=?", (userid,))
        self.connection.commit()

    def delete_notes(self, userid):
        self.cursor.execute("DELETE FROM notes WHERE userid=?", (userid,))
        self.connection.commit()
