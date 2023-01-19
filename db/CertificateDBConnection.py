import sqlite3


class CertificateDBConnection(object):
    instance = None

    @staticmethod
    def Instance():
        try:
            if CertificateDBConnection.instance is None:
                CertificateDBConnection.instance = sqlite3.connect("certificates_bd.db")
            return CertificateDBConnection.instance

        except AttributeError:
            return 'Database connection object creation error'
