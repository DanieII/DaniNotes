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
        # self.cursor.execute("""CREATE TABLE if not exists notes (
        #                     noteid INTEGER PRIMARY KEY AUTOINCREMENT,
        #                     userid TEXT REFERENCES users(userid),
        #                     note_title TEXT,
        #                     note_data TEXT
        #                     )""")
        # c.execute("SELECT * FROM users")
        # result = c.fetchall()
        # print(result)
        self.connection.commit()

    def get_user_data(self, username):
        current_data = self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        return current_data

    def add_user(self, user, password):
        try:
            self.cursor.execute("""INSERT INTO users(username,password)
                                    VALUES(?,?)""", (user, password))
            self.connection.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def delete_users(self, user_to_delete):
        self.cursor.execute("""DELETE FROM users WHERE username=?""", (user_to_delete,))
        self.connection.commit()
