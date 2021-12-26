import unittest

from databases.database import Database

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database("../../Database/unittest_test_database.db")

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
