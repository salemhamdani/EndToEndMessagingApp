from db.user_db_connection import UserDbConnection


class UserRepository:
    @staticmethod
    def init_table():
        connection = UserDbConnection.get_instance()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (cart_id text PRIMARY KEY, name text, pseudo text UNIQUE, salt text, password text)
        ''')
        return cursor

    @staticmethod
    def insert_user(user):
        cursor = UserRepository.init_table()
        cursor.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
            (user['cart_id'], user['name'], user['pseudo'], user['salt'], user['password'])
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
