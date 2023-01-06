import sqlite3 as sql


class Database:
    def create_tables(self):
        conn = sql.connect("my_database.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists users (
                            userid INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            password TEXT
                            )""")
        # c.execute("""CREATE TABLE if not exists notes (
        #                     noteID integer AUTOINCREMENT,
        #                     userID TEXT,
        #                     PRIMARY KEY(noteID),
        #                     FOREIGN KEY(userID) REFERENCES users(noteID)
        #                     )""")
        # c.execute("""CREATE TABLE if not exists notes_data (
        #                         dataID integer AUTOINCREMENT,
        #                         noteID integer,
        #                         PRIMARY KEY(dataID),
        #                         FOREIGN KEY(noteID) REFERENCES notes(noteID)
        #                         )""")
        # c.execute("SELECT * FROM users")
        # result = c.fetchall()
        # print(result)
        conn.commit()
        conn.close()

    def add_user(self, user, password):
        conn = sql.connect("my_database.db")
        c = conn.cursor()

        c.execute("""INSERT INTO users(username,password)
                        VALUES(?,?)""", (user, password))
        conn.commit()
        conn.close()

    def delete_users(self, user_to_delete):
        conn = sql.connect("my_database.db")
        c = conn.cursor()

        c.execute("""DELETE FROM users WHERE username=?""", (user_to_delete,))
        conn.commit()
        conn.close()
