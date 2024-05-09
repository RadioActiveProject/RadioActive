import sqlite3
from sqlite3 import Connection
import os
from shutil import copyfile
from dataclasses import dataclass

DB_FOLDER = 'database'
DB_USERS_PATH = DB_FOLDER + "/users.db"

def get_db_connection() -> Connection:
    if not os.path.exists(DB_USERS_PATH):
        os.makedirs(DB_USERS_PATH)

    return sqlite3.connect(DB_USERS_PATH)


def initialize_users_db() -> None:
    if os.path.isfile(DB_USERS_PATH):
        return
        os.remove(DB_USERS_PATH)
    conn = sqlite3.connect(DB_USERS_PATH)
    conn.cursor().executescript(
        """
            CREATE TABLE IF NOT EXISTS users (
                EMAIL TEXT NOT NULL,
                PASSWORD TEXT NOT NULL,
                NAME TEXT NOT NULL,
                IS_DEVELOPER BOOLEAN NOT NULL,
                STATUS TEXT NOT NULL,
                PRIMARY KEY (EMAIL)
            );
        """
    )
    conn.commit()
    conn.close()


@dataclass
class User:
    email: str
    password: str
    name: str
    is_developer: bool
    status: str

    def __str__(self):
        params = map(lambda x:f"'{x}'", [self.email, self.password, self.name, self.is_developer, self.status])
        return '(' + ', '.join(params) + ')'

def get_user_from_email(email: str, path:str = DB_USERS_PATH) -> User:
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE EMAIL = ?",
        (email,)
    )
    result = cur.fetchone()
    conn.close()
    if result is None:
        return None
    return User(*result)

def get_user_from_db(email: str) -> User:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE EMAIL = ?",
        (email,)
    )
    result = cur.fetchone()
    conn.close()
    if result is None:
        return None
    return User(*result)


def register(user: User, path:str = DB_USERS_PATH) -> None:
    conn = sqlite3.connect(path)
    conn.cursor().execute(
        "INSERT INTO users (EMAIL, PASSWORD, NAME, IS_DEVELOPER, STATUS) VALUES " + str(user)
    )
    conn.commit()
    conn.close()


def update_status(email: str, status: str):
    """
    updates the status of a given user, has a sql injection vulnerability
    :param user:
    :param status:
    :param path:
    :return:
    """
    conn = get_db_connection()
    # I need to ask my senior engineer if it's okay, I found it on the internet and I'm not sure it's secure
    conn.cursor().execute(
        f"UPDATE users SET status = '{status}' WHERE email = '{email}'"
    )
    conn.commit()
    conn.close()



