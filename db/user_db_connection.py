import sqlite3


class UserDbConnection(object):
    instance = None

    @staticmethod
    def get_instance():
        try:
            if UserDbConnection.instance is None:
                UserDbConnection.instance = sqlite3.connect("./db/users_bd.db")
            return UserDbConnection.instance

        except AttributeError:
            return 'User database connection object creation error'
