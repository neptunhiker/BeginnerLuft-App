import unittest

from tools.helpers import string_to_float

class StringToFlaot(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
