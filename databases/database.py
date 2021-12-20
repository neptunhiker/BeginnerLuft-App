import sqlite3
from contextlib import closing
import datetime

from tools import helpers
from tools import custom_exceptions


class Database:
    """A class for establishing a connection to a data base"""

    def __init__(self, database_path):
        self.database_path = database_path
        self.conn = None

    def connect_to_database(self):
        """Establish the connection to the data base"""

        self.conn = sqlite3.connect(self.database_path)
        self.conn.row_factory = sqlite3.Row

    @classmethod
    def test_database(cls):
        return cls(database_path="../../Database/test_database.db")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.database_path})"


if __name__ == '__main__':
    test_db = Database.test_database()
    print(test_db)
