from db.user_db_connection import UserDbConnection


class UserRepository:
    @staticmethod
    def init_table():
        connection = UserDbConnection.get_instance()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (cart_id text PRIMARY KEY, name text, pseudo text UNIQUE, salt text, password text, connected number)
        ''')
        return cursor

    @staticmethod
    def insert_user(user):
        cursor = UserRepository.init_table()
        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)",
            (user['cart_id'], user['name'], user['pseudo'], user['salt'], user['password'], 0)
        )
        UserDbConnection.get_instance().commit()

    @staticmethod
    def get_by_pseudo(pseudo):
        cursor = UserRepository.init_table()
        cursor.execute(
            "SELECT password, salt FROM users WHERE pseudo like ?",
            (pseudo.decode(),)
        )
        return cursor.fetchone()

    @staticmethod
    def get_connected_users():
        cursor = UserRepository.init_table()
        cursor.execute("SELECT pseudo FROM users WHERE connected = 1")
        return cursor.fetchall()

    @staticmethod
    def connect(pseudo):
        cursor = UserRepository.init_table()
        cursor.execute("UPDATE users set connected = 1 WHERE pseudo LIKE ?", (pseudo.decode(),))
        UserDbConnection.get_instance().commit()

    @staticmethod
    def disconnect(pseudo):
        cursor = UserRepository.init_table()
        cursor = UserRepository.init_table()
        cursor.execute("UPDATE users set connected = 0 WHERE pseudo LIKE ?", (pseudo.decode(),))
        UserDbConnection.get_instance().commit()
