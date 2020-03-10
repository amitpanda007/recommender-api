from mysql.connector import connect, Error
from rec_app import settings


def run_query(query):
    db = MySQLDatabaseConnector()
    cursor = db.connect_db()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


class MySQLDatabaseConnector(object):

    def __init__(self):
        self.host = settings.MYSQL_HOST
        self.database = settings.MYSQL_DATABASE
        self.user = settings.MYSQL_USER
        self.password = settings.MYSQL_PASSWORD
        self._connection = None
        self._cursor = None

    def get_connection(self):
        return self._connection

    def connect_db(self):
        try:
            self._connection = connect(host=self.host, database=self.database, user=self.user, password=self.password)
            self._cursor = self._connection.cursor()
            cursor = self._cursor
            return cursor
        except Error as error:
            print("Failed to insert record into user_ratings table {}".format(error))
            if self._connection.is_connected():
                self._connection.close()

    def close_db(self):
        if self._connection.is_connected():
            self._connection.close()

