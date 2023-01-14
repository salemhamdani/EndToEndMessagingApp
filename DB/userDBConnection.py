import sqlite3


class UserDBConnection(object):
    instance = None

    @staticmethod
    def Instance():
        try:
            if UserDBConnection.instance is None:
                UserDBConnection.instance = sqlite3.connect("users_bd.db")
            return UserDBConnection.instance

        except AttributeError:
            return 'User database connection object creation error'
