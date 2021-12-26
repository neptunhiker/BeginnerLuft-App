"""
Tests that cover the helper functions in tools.helpers
"""

import datetime
import unittest

from tools.custom_exceptions import DateFormatException
from tools import helpers


class CheckIfFileExists(unittest.TestCase):

    def test_happy_path(self):
        path = f"{__name__}.py"
        target_output = True
        output = helpers.check_if_file_exists(path)
        self.assertEqual(target_output, output)

    def test_non_happy_path(self):
        path = "something"
        target_output = False
        output = helpers.check_if_file_exists(path)
        self.assertEqual(target_output, output)

        path_to_file = 23
        self.assertRaises(TypeError, helpers.check_if_file_exists, path_to_file)


class CreateInvoiceNr(unittest.TestCase):

    def test_happy_path(self):
        date = datetime.date(2021, 8, 4)
        output = helpers.create_invoice_nr(creation_date=date, participant_first_name="Mohammed",
                                           participant_last_name="Ali")
        target_output = "2021-08-04-MA"
        self.assertEqual(target_output, output)

        date = "12.03.2021"
        output = helpers.create_invoice_nr(creation_date=date, participant_first_name="Mohammed",
                                           participant_last_name="Ali")
        target_output = "2021-03-12-MA"
        self.assertEqual(target_output, output)

        date = "2022-2-3"
        output = helpers.create_invoice_nr(creation_date=date, participant_first_name="Mohammed",
                                           participant_last_name="Ali")
        target_output = "2022-02-03-MA"
        self.assertEqual(target_output, output)

    def test_non_happy_path(self):
        first_name = "Casius"
        last_name = "Clay"
        date = "something"
        self.assertRaises(DateFormatException, helpers.create_invoice_nr, date, first_name, last_name)

        first_name = ""
        last_name = "Clay"
        date = "2021-02-12"
        self.assertRaises(AttributeError, helpers.create_invoice_nr, date, first_name, last_name)

        first_name = "Casius"
        last_name = ""
        date = "2021-02-12"
        self.assertRaises(AttributeError, helpers.create_invoice_nr, date, first_name, last_name)

        first_name = ""
        last_name = ""
        date = "2021-02-12"
        self.assertRaises(AttributeError, helpers.create_invoice_nr, date, first_name, last_name)


class TestCreateInvoiceName(unittest.TestCase):

    def test_happy_path(self):
        participant_first_name = "Rachel"
        participant_last_name = "Robinson"

        creation_date = datetime.date(2021, 3, 8)
        output = helpers.create_invoice_name(creation_date, participant_first_name, participant_last_name)
        target_output = "2021-03-08 Rechnung Rachel Robinson"
        self.assertEqual(target_output, output)

        creation_date = "09.3.2021"
        output = helpers.create_invoice_name(creation_date, participant_first_name, participant_last_name)
        target_output = "2021-03-09 Rechnung Rachel Robinson"
        self.assertEqual(target_output, output)

    def test_non_happy_path(self):
        creation_date = ""
        self.assertRaises(DateFormatException, helpers.create_invoice_name, creation_date, "Rachel", "Robinson")

        creation_date = "something"
        self.assertRaises(DateFormatException, helpers.create_invoice_name, creation_date, "Rachel", "Robinson")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, helpers.create_invoice_name, creation_date, "", "Robinson")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, helpers.create_invoice_name, creation_date, "Ben", "")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, helpers.create_invoice_name, creation_date, "", "")


class DeterminePaymentTargetDate(unittest.TestCase):

    def test_happy_path(self):
        date = datetime.date(year=2021, month=2, day=26)
        target_output = datetime.date(year=2021, month=3, day=12)
        func_output = helpers.determine_payment_target_date(starting_date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=12, day=23)
        target_output = datetime.date(year=2022, month=1, day=6)
        func_output = helpers.determine_payment_target_date(starting_date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=10, day=16)
        target_output = datetime.date(year=2021, month=11, day=1)
        func_output = helpers.determine_payment_target_date(starting_date=date, payment_horizon_in_days=14)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2022, month=1, day=12)
        target_output = datetime.date(year=2022, month=1, day=31)
        func_output = helpers.determine_payment_target_date(starting_date=date, payment_horizon_in_days=17)
        self.assertEqual(func_output, target_output)

    def test_non_happy_path(self):
        date = "2021-05-12"
        payment_horizon_in_days = 14
        self.assertRaises(TypeError, helpers.determine_payment_target_date, date, payment_horizon_in_days)

        date = "some string"
        payment_horizon_in_days = 14
        self.assertRaises(TypeError, helpers.determine_payment_target_date, date, payment_horizon_in_days)

        date = datetime.date(year=2022, month=1, day=12)
        payment_horizon_in_days = "14"
        self.assertRaises(TypeError, helpers.determine_payment_target_date, date, payment_horizon_in_days)


class FormatToGermanDate(unittest.TestCase):

    def test_happy_path(self):
        date = datetime.date(year=1984, month=1, day=31)
        target_output = "31. Januar 1984"
        func_output = helpers.format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=1990, month=2, day=1)
        target_output = "01. Februar 1990"
        func_output = helpers.format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=3, day=9)
        target_output = "09. März 2021"
        func_output = helpers.format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=8, day=4)
        target_output = "04. August 2021"
        func_output = helpers.format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

        date = datetime.date(year=2021, month=10, day=19)
        target_output = "19. Oktober 2021"
        func_output = helpers.format_to_german_date(date=date)
        self.assertEqual(func_output, target_output)

    def test_non_happy_path(self):
        date = "2021-06-03"
        self.assertRaises(AttributeError, helpers.format_to_german_date, date)


class ParseDateFromString(unittest.TestCase):

    def test_happy_path(self):
        datestring = "2021-10-22"
        target_output = datetime.date(year=2021, month=10, day=22)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-10-22"
        target_output = datetime.date(year=2021, month=10, day=22)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-1-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-1-8"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-1-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-1-8"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.04.2021"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.4.2021"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.04.21"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "03.04.2021"
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "3.4.2021"
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = " 3.4.2021  "  # whitespace
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = helpers.parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

    def test_non_happy_path(self):
        datestring = "something"
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)

        datestring = "2021-03-044"  # typo at the end of the datestring
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)

        datestring = ""
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)

        datestring = "10.03.201"
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)

        datestring = "10.03."
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)

        datestring = "10/03/2021"
        self.assertRaises(DateFormatException, helpers.parse_date_from_string, datestring)


class PasswordMinRequirements(unittest.TestCase):

    def test_happy_path(self):

        password = "lasdflKJn23"
        target_output = True
        output = helpers.password_min_requirements(password)
        self.assertEqual(target_output, output)

        password = "dja"
        target_output = False
        output = helpers.password_min_requirements(password)
        self.assertEqual(target_output, output)

        password = "jd klsd"
        target_output = False
        output = helpers.password_min_requirements(password)
        self.assertEqual(target_output, output)

        password = "sda "
        target_output = False
        output = helpers.password_min_requirements(password)
        self.assertEqual(target_output, output)

        password = " d d"
        target_output = False
        output = helpers.password_min_requirements(password)
        self.assertEqual(target_output, output)

    def test_non_happy_path(self):

        password = 13423
        self.assertRaises(TypeError, helpers.password_min_requirements, password)

class StringToFloat(unittest.TestCase):

    def test_simple_cases(self):
        """Test normal conversion of string to float"""

        string = 23.34
        output = helpers.string_to_float(string)
        target_output = 23.34
        self.assertEqual(output, target_output)

        string = "102,32"
        output = helpers.string_to_float(string)
        target_output = 102.32
        self.assertEqual(output, target_output)

        string = "10.12"
        output = helpers.string_to_float(string)
        target_output = 10.12
        self.assertEqual(output, target_output)

    def test_complex_cases(self):
        string = "10.000,23"
        output = helpers.string_to_float(string)
        target_output = 10000.23
        self.assertEqual(output, target_output)

        string = "10.000.321,23"
        output = helpers.string_to_float(string)
        target_output = 10000321.23
        self.assertEqual(output, target_output)

        string = "12,345,654.22"
        output = helpers.string_to_float(string)
        target_output = 12345654.22
        self.assertEqual(output, target_output)

        string = "10,234.56"
        output = helpers.string_to_float(string)
        target_output = 10234.56
        self.assertEqual(output, target_output)


class VerifyPassword(unittest.TestCase):

    def test_happy_path(self):

        password = "123456asdfJKLÖ"
        hashed_password = helpers.hash_password(password=password)
        target_output = True
        self.assertEqual(target_output, helpers.verify_password(stored_password=hashed_password,
                                                                provided_password=password))

        password = "987asdf23!§$kiUZ"
        hashed_password = helpers.hash_password(password=password)
        target_output = False
        self.assertEqual(target_output, helpers.verify_password(stored_password=hashed_password,
                                                                provided_password="something else"))

        password = "    hello          "
        hashed_password = helpers.hash_password(password=password)
        target_output = True
        self.assertEqual(target_output, helpers.verify_password(stored_password=hashed_password,
                                                                provided_password=password))

    def test_non_happy_path(self):
        password = 123
        self.assertRaises(AttributeError, helpers.verify_password, "stored password", password)



if __name__ == '__main__':
    unittest.main()
