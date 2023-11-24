import sqlite3
import bcrypt


class BerestaDatabase:

    _name = ""
    _con = ""
    _cur = ""

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
           userlogin TEXT PRIMARY KEY,
           password TEXT)
        """)
        self._con.commit()
        return

    def _hash_password(self, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')

    def insert_user(self, userlogin: str, password: str):
        user = (userlogin, self._hash_password(password))
        query = "SELECT * FROM users WHERE userlogin = ?"
        print(self.in_db(userlogin))
        print(self._cur.execute(query, (userlogin, )).fetchone())
        query = "INSERT INTO users VALUES(?, ?);"
        if not self.in_db(userlogin):
            self._cur.execute(query, user)
            self._con.commit()
            return True

        return False

    def in_db(self, userlogin: str):
        query = 'SELECT * FROM users WHERE userlogin = ?'
        if self._cur.execute(query, (userlogin, )).fetchone() is None:
            return False

        return True

    def get_user(self, userlogin: str):
        query = 'SELECT * FROM users WHERE userlogin = ? LIMIT 1'
        return self._cur.execute(query, (userlogin, )).fetchone()

    def check_password(self, userlogin: str, password: str):
        query = "SELECT * FROM users WHERE userlogin = ?"
        if self.in_db(userlogin):
            _passw = self._cur.execute(query, (userlogin, )).fetchone()[1]
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
            update_query = "UPDATE users SET userlogin = ? WHERE userlogin = ? AND password = ?"
            self._cur.execute(update_query, (userlogin_new, userlogin_old, self._hash_password(password)))
            self._con.commit()
            return True

        return False

    def change_password(self, userlogin: str, password_new: str, password_old: str):
        if self.check_password(userlogin, password_old):
            update_query = "UPDATE users SET password = ? WHERE userlogin = ? AND password = ?"
            self._cur.execute(update_query, (self._hash_password(password_new), userlogin, self._hash_password(password_old)))
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
