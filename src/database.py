import pathlib
import sqlite3
from sqlite3 import IntegrityError
import bcrypt
from models.user import User


# Sqlite3 access
class Database:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    # initialize database on file_path, create cursor
    def __init__(self, file_path=pathlib.Path("src", "movie-manager.db")):
        self.file_path = file_path
        self.con = sqlite3.connect(self.file_path)
        self.cur = self.con.cursor()

    def fetch_user_by_email(self, email):
        self.cur.execute(f'SELECT * FROM users WHERE email LIKE "{email}"')
        res = self.cur.fetchall()
        # print(len(res))
        if len(res) != 1:
            raise Exception("ERROR: user not found " + email)
        else:
            watched_ids = self.fetch_watched_by_email(email)
            watchlist_ids = self.fetch_watchlist_by_email(email)
            # print(User(res[0][0], res[0][1], watched_ids, watchlist_ids))
            return User(res[0][0], res[0][1], watched_ids, watchlist_ids)

    def create_user(self, username, email, password):
        self.cur.execute(f'SELECT * FROM users WHERE email LIKE "{email}"')
        if len(self.cur.fetchall()) == 1:
            return False

        self.cur.execute(f'INSERT INTO users VALUES ( "{username}", "{email}", "{self.hash_pw(password).decode("utf-8")}" )')
        self.con.commit()
        if self.cur.rowcount == 1:
            print("User successfully created")
            return True

    def fetch_watched_by_email(self, email):
        self.cur.execute(f'SELECT movie_id FROM watched WHERE email LIKE "{email}"')
        res = self.cur.fetchall()
        return [x[0] for x in res]

    def fetch_watchlist_by_email(self, email):
        self.cur.execute(f'SELECT movie_id FROM watchlist WHERE email LIKE "{email}"')
        res = self.cur.fetchall()
        return [x[0] for x in res]

    def delete_from_watched(self, email, movie_id):
        self.cur.execute(f'DELETE FROM watched WHERE email LIKE "{email}" AND movie_id = {movie_id}')
        self.con.commit()
        if self.cur.rowcount:
            print(f"Movie {movie_id} successfully removed from watched list.")
        else:
            print(f"Movie {movie_id} isn't in the watched list.")

    def delete_from_watchlist(self, email, movie_id):
        self.cur.execute(f'DELETE FROM watchlist WHERE email LIKE "{email}" AND movie_id = {movie_id}')
        self.con.commit()
        if self.cur.rowcount:
            print(f"Movie {movie_id} successfully removed from watchlist.")
        else:
            print(f"Movie {movie_id} isn't in the watchlist.")

    def add_to_watched(self, email, movie_id):
        # maybe they had it on their watchlist?
        self.delete_from_watchlist(email, movie_id)
        try:
            self.cur.execute(f'INSERT INTO watched VALUES ( "{email}", {movie_id} )')
            self.con.commit()
        except IntegrityError:
            print("Already added.")
            return False
        else:
            print(f"Movie {movie_id} successfully added to watched.")
            return True

    def add_to_watchlist(self, email, movie_id):
        try:
            self.cur.execute(f'INSERT INTO watchlist VALUES ( "{email}", {movie_id} )')
            self.con.commit()
        except IntegrityError:
            print("Already added.")
            return False
        else:
            print(f"Movie {movie_id} successfully added to watchlist.")
            return True

    @staticmethod
    def hash_pw(password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def create_tables(self):
        self.cur.execute(
            'CREATE TABLE users ( username VARCHAR(64), email VARCHAR(64) PRIMARY KEY, enc_password TEXT )')
        self.cur.execute('CREATE TABLE watched ( email VARCHAR(64), movie_id INTEGER, PRIMARY KEY (email, movie_id) )')
        self.cur.execute('CREATE TABLE watchlist ( email VARCHAR(64), movie_id INTEGER, PRIMARY KEY (email, movie_id) )')
        self.cur.execute(
            f'INSERT INTO users VALUES ("dummy_username", "dummy_email@gmail.com", "{self.hash_pw("123456")}")')
        self.cur.execute('INSERT INTO watched VALUES ("dummy_email@gmail.com", 1)')
        self.cur.execute('INSERT INTO watched VALUES ("dummy_email@gmail.com", 3)')
        self.cur.execute('INSERT INTO watchlist VALUES ("dummy_email@gmail.com", 5)')
        self.cur.execute('INSERT INTO watchlist VALUES ("dummy_email@gmail.com", 70)')
        self.cur.execute('INSERT INTO watchlist VALUES ("dummy_email@gmail.com", 29)')
        self.con.commit()

    # return User or False if credentials are incorrect
    def verify_credentials(self, username_or_email, password):
        self.cur.execute(f'SELECT * FROM users WHERE username LIKE "{username_or_email}" OR email LIKE "{username_or_email}"')
        res = self.cur.fetchall()
        # print(res)
        if len(res) == 0:
            return False
        for result in res:
            user_data = result
            if bcrypt.checkpw(password.encode('utf-8'), user_data[2].encode('utf-8')):
                user = User(user_data[0], user_data[1],
                            self.fetch_watched_by_email(user_data[1]),
                            self.fetch_watchlist_by_email(user_data[1]))
                return user
        return False

    # check if user alraedy exists with email or username named param
    def user_exists(self, email='', username=''):
        if email == '' and username == '':
            return True
        if email != '':
            self.cur.execute(f'SELECT * FROM users WHERE email LIKE "{email}"')
            res = self.cur.fetchall()
            if len(res) == 0:
                return False
            return True
        if username != '':
            self.cur.execute(f'SELECT * FROM users WHERE username LIKE "{username}"')
            res = self.cur.fetchall()
            if len(res) == 0:
                return False
            return True
