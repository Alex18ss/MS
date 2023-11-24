import random
import sqlite3
import string
import bcrypt
from datetime import datetime


class BerestaDatabase:
    _name = ""
    _con = ""
    _cur = ""

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def __init__(self, name: str):
        self._name = name
        self.connect()
        self.create_table()

    def get_name(self):
        return self._name

    def set_database(self, name: str):
        self.close()
        self._name = name
        self.connect()
        return

    def connect(self):
        self._con = sqlite3.connect(self._name, check_same_thread=False)
        self._cur = self._con.cursor()
        return

    def close(self):
        self._con.close()
        self._cur.close()

    def create_table(self):
        self._cur.execute("""CREATE TABLE IF NOT EXISTS users(
                   userLogin TEXT PRIMARY KEY,
                   password TEXT,
                   session TEXT,
                   sessionCreated DATE
                   )
                """)
        self._con.commit()
        return

    def _hash_password(self, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def insert_user(self, user_login: str, password: str):
        user = (user_login, self._hash_password(password), self.id_generator(40), str(datetime.now().date()))
        query = "SELECT * FROM users WHERE userLogin = ?"
        print(self.in_db(user_login))
        print(self._cur.execute(query, (user_login,)).fetchone())
        query = "INSERT INTO users VALUES(?, ?, ?, ?);"
        if not self.in_db(user_login):
            self._cur.execute(query, user)
            self._con.commit()
            return True

        return False

    def get_session(self, user_login: str):
        print("gs", user_login)
        query = 'SELECT session FROM users WHERE userlogin = ?'
        return self._cur.execute(query, (user_login,)).fetchone()[0]

    def in_db(self, user_login: str):
        query = 'SELECT * FROM users WHERE userLogin = ?'
        if self._cur.execute(query, (user_login,)).fetchone() is None:
            return False

        return True

    def refresh_session(self, user_login: str):
        query = 'UPDATE users SET session = ?, sessionCreated = ? WHERE userLogin = ?'
        self._cur.execute(query, (self.id_generator(40), str(datetime.now().date()), user_login))
        self._con.commit()


    def get_user(self, session: str):
        query = 'SELECT * FROM users WHERE session = ? LIMIT 1'
        return self._cur.execute(query, (session,)).fetchone()

    def check_password(self, user_login: str, password: str):
        query = "SELECT * FROM users WHERE userLogin = ?"
        if self.in_db(user_login):
            _passw = self._cur.execute(query, (user_login,)).fetchone()[1]
            return bcrypt.checkpw(password.encode('utf-8'), _passw.encode('utf-8'))

    def recreate_table(self):
        self._cur.execute("""DROP TABLE users""")
        self._con.commit()
        self.create_table()
        self._con.commit()

    def delete_table(self):
        self._cur.execute("""DROP TABLE users""")
        self._con.commit()

    def change_userlogin(self, userlogin_old: str, userlogin_new: str, password: str):
        if self.check_password(userlogin_old, password):
            update_query = "UPDATE users SET userLogin = ? WHERE userLogin = ? AND password = ?"
            self._cur.execute(update_query, (userlogin_new, userlogin_old, self._hash_password(password)))
            self._con.commit()
            return True

        return False

    def change_password(self, userlogin: str, password_new: str, password_old: str):
        if self.check_password(userlogin, password_old):
            update_query = "UPDATE users SET password = ? WHERE userLogin = ? AND password = ?"
            self._cur.execute(update_query,
                              (self._hash_password(password_new), userlogin, self._hash_password(password_old)))
            self._con.commit()
            return True

        return False

    def print_db(self):
        print(*self._cur.execute("SELECT * FROM users;").fetchone())


if __name__ == "__main__":
    print("Database name: ")
    name = str(input())

    db = BerestaDatabase(name)
    db.recreate_table()

    print("User login: ")
    login = input()
    print("Username: ")
    username = input()
    print("Password: ")
    password = input()

    db.insert_user(login, username, password)

    db.print_db()

    print("New password: ")
    np = input()
    print(db.check_password(login, username, np))

    db.change_password(login, username, np, password)
    db.print_db()

    db.delete_table()
