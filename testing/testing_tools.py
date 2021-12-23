import datetime
import unittest

from objects.invoice import Invoice
from tools.custom_exceptions import DateFormatException
from tools import helpers
from tools.helpers import create_invoice_name, create_invoice_nr, parse_date_from_string, string_to_float


class StringToFloat(unittest.TestCase):

    def test_simple_cases(self):
        """Test normal conversion of string to float"""

        string = 23.34
        output = string_to_float(string)
        target_output = 23.34
        self.assertEqual(output, target_output)

        string = "102,32"
        output = string_to_float(string)
        target_output = 102.32
        self.assertEqual(output, target_output)

        string = "10.12"
        output = string_to_float(string)
        target_output = 10.12
        self.assertEqual(output, target_output)

    def test_complex_cases(self):
        string = "10.000,23"
        output = string_to_float(string)
        target_output = 10000.23
        self.assertEqual(output, target_output)

        string = "10.000.321,23"
        output = string_to_float(string)
        target_output = 10000321.23
        self.assertEqual(output, target_output)

        string = "12,345,654.22"
        output = string_to_float(string)
        target_output = 12345654.22
        self.assertEqual(output, target_output)

        string = "10,234.56"
        output = string_to_float(string)
        target_output = 10234.56
        self.assertEqual(output, target_output)


class InvoiceNrCreation(unittest.TestCase):

    def test_invoice_nr_creation(self):
        date = datetime.date(2021, 8, 4)
        output = create_invoice_nr(creation_date=date, participant_first_name="Mohammed", participant_last_name="Ali")
        target_output = "2021-08-04-MA"
        self.assertEqual(target_output, output)

        date = "12.03.2021"
        output = create_invoice_nr(creation_date=date, participant_first_name="Mohammed", participant_last_name="Ali")
        target_output = "2021-03-12-MA"
        self.assertEqual(target_output, output)


        date = "2022-2-3"
        output = create_invoice_nr(creation_date=date, participant_first_name="Mohammed", participant_last_name="Ali")
        target_output = "2022-02-03-MA"
        self.assertEqual(target_output, output)


class TestParseDateString(unittest.TestCase):

    def test_parse_date_string(self):
        datestring = "2021-10-22"
        target_output = datetime.date(year=2021, month=10, day=22)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-10-22"
        target_output = datetime.date(year=2021, month=10, day=22)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-1-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-1-8"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "2021-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-1-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-1-8"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "21-01-08"
        target_output = datetime.date(year=2021, month=1, day=8)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.04.2021"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.4.2021"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "23.04.21"
        target_output = datetime.date(year=2021, month=4, day=23)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "03.04.2021"
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = "3.4.2021"
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

        datestring = " 3.4.2021  "  # whitespace
        target_output = datetime.date(year=2021, month=4, day=3)
        func_output = parse_date_from_string(datestring)
        self.assertEqual(func_output, target_output)

    def test_bad_input(self):
        datestring = "something"
        self.assertRaises(DateFormatException, parse_date_from_string, datestring)

        datestring = "2021-03-044"  # typo at the end of the datestring
        self.assertRaises(DateFormatException, parse_date_from_string, datestring)

        datestring = ""
        self.assertRaises(DateFormatException, parse_date_from_string, datestring)

        datestring = "10.03.201"
        self.assertRaises(DateFormatException, parse_date_from_string, datestring)


class InvoiceName(unittest.TestCase):

    def test_good_input(self):

        creation_date = datetime.date(2021, 3, 8)
        participant_first_name = "Rachel"
        participant_last_name = "Robinson"
        output = create_invoice_name(creation_date, participant_first_name, participant_last_name)
        target_output = "2021-03-08 Rechnung Rachel Robinson"
        self.assertEqual(target_output, output)

        creation_date = "09.3.2021"
        participant_first_name = "Rachel"
        participant_last_name = "Robinson"
        output = create_invoice_name(creation_date, participant_first_name, participant_last_name)
        target_output = "2021-03-09 Rechnung Rachel Robinson"
        self.assertEqual(target_output, output)

    def test_bad_input(self):
        creation_date = ""
        self.assertRaises(AttributeError, create_invoice_name, creation_date, "Rachel", "Robinson")

        creation_date = "something"
        self.assertRaises(AttributeError, create_invoice_name, creation_date, "Rachel", "Robinson")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, create_invoice_name, creation_date, "", "Robinson")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, create_invoice_name, creation_date, "Ben", "")

        creation_date = "12.03.2021"
        self.assertRaises(AttributeError, create_invoice_name, creation_date, "", "")


class FileExists(unittest.TestCase):
    """Check if a file exists"""

    def test_happy_path(self):
        path_to_file = "testing_tools.py"
        output = helpers.check_if_file_exists(path_to_file)
        target_output = True
        self.assertEqual(target_output, output)

        path_to_file = "nonexistingfile.xls"
        output = helpers.check_if_file_exists(path_to_file)
        target_output = False
        self.assertEqual(target_output, output)

        path_to_file = "random something"
        output = helpers.check_if_file_exists(path_to_file)
        target_output = False
        self.assertEqual(target_output, output)

    def test_non_happy_path(self):
        path_to_file = 23
        self.assertRaises(TypeError, helpers.check_if_file_exists, path_to_file)


if __name__ == '__main__':
    unittest.main()
