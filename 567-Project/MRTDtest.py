import unittest
from unittest.mock import patch, MagicMock
from MRTD import MRZProcessor

class TestMRZProcessor(unittest.TestCase):
    def setUp(self):
        # Initialize MRZProcessor before each test
        self.processor = MRZProcessor()

    def test_scan_mrz(self):
        """
        Test that scan_mrz correctly stores the provided MRZ lines.
        """
        line1 = "P<TJKCOMBS<<ADDISON<JANE<<<<<<<<<<<<<<<<<<<<"
        line2 = "V855996J79TJK7209167M0905071MI797251T<<<<<<7"
        self.processor.scan_mrz(line1, line2)
        self.assertEqual(self.processor.line1, line1)
        self.assertEqual(self.processor.line2, line2)

    def test_decode_mrz(self):
        """
        Test that decode_mrz correctly decodes MRZ data into fields using Damm algorithm for check digits.
        """
        data = {
            "Document Type": "P",
            "Issuing Country": "TJK",
            "Name": "COMBS<<ADDISON<JANE",
            "Passport Number": "V855996J7",
            "Nationality": "TJK",
            "Date of Birth": "720916",
            "Gender": "M",
            "Expiration Date": "090507",
            "Personal Number": "MI797251T"
        }
        # Encode MRZ lines using the data
        line1, line2 = self.processor.encode_mrz(data)
        self.processor.scan_mrz(line1, line2)
        result = self.processor.decode_mrz()
        expected = {
            "Document Type": "P",
            "Issuing Country": "TJK",
            "Name": "COMBS ADDISON JANE",
            "Passport Number": "V855996J7",
            "Nationality": "TJK",
            "Date of Birth": "720916",
            "Gender": "M",
            "Expiration Date": "090507",
            "Personal Number": "MI797251T"
        }
        self.assertEqual(result, expected)

    def test_encode_mrz(self):
        """
        Test that encode_mrz correctly encodes data into MRZ format.
        """
        data = {
            "Document Type": "P",
            "Issuing Country": "TJK",
            "Name": "COMBS<<ADDISON<JANE",
            "Passport Number": "V855996J7",
            "Nationality": "TJK",
            "Date of Birth": "720916",
            "Gender": "M",
            "Expiration Date": "090507",
            "Personal Number": "MI797251T"
        }
        line1, line2 = self.processor.encode_mrz(data)
        self.assertTrue(line1.startswith("P<TJKCOMBS"))
        self.assertTrue(line2.startswith("V855996J7"))

    def test_validate_check_digit(self):
        """
        Test that validate_check_digit correctly validates check digits.
        """
        result = self.processor.validate_check_digit("123456789", '4', "passport number", 2)
        self.assertTrue(result)

    def test_calculate_check_digit(self):
        """
        Test that calculate_check_digit correctly calculates the check digit using the Damm algorithm.
        """
        check_digit = self.processor.calculate_check_digit("123456789")
        self.assertEqual(check_digit, '4')  # Expected check digit is '4'

    def test_retrieve_from_database(self):
        """
        Test that retrieve_from_database returns expected dummy data.
        """
        data = self.processor.retrieve_from_database("L898902C3")
        self.assertEqual(data["Passport Number"], "L898902C3")

    def test_write_to_database(self):
        """
        Test that write_to_database does not raise any exceptions.
        """
        data = {"Sample": "Data"}
        try:
            self.processor.write_to_database(data)
        except Exception as e:
            self.fail(f"write_to_database raised an exception {e}")

    def test_hardware_scan(self):
        """
        Test that hardware_scan correctly simulates scanning and sets MRZ lines.
        """
        self.processor.hardware_scan()
        self.assertIsNotNone(self.processor.line1)
        self.assertIsNotNone(self.processor.line2)

    def test_decode_mrz_invalid_check_digit(self):
        """
        Test decode_mrz with incorrect final check digit.
        """
        data = {
            "Document Type": "P",
            "Issuing Country": "TJK",
            "Name": "COMBS<<ADDISON<JANE",
            "Passport Number": "V855996J7",
            "Nationality": "TJK",
            "Date of Birth": "720916",
            "Gender": "M",
            "Expiration Date": "090507",
            "Personal Number": "MI797251T"
        }
        # Generate MRZ lines with correct check digits
        line1, line2 = self.processor.encode_mrz(data)
        # Introduce an incorrect final check digit
        line2 = line2[:-1] + '9'  # Replace the last character with '9'
        self.processor.scan_mrz(line1, line2)
        result = self.processor.decode_mrz()
        self.assertEqual(result, "Check digit validation failed for personal number.")

    def test_decode_mrz_missing_data(self):
        """
        Test decode_mrz when MRZ data is missing.
        """
        self.processor.scan_mrz("", "")
        result = self.processor.decode_mrz()
        self.assertEqual(result, "Error: MRZ data is missing.")

    def test_calculate_check_digit_non_numeric(self):
        """
        Test calculate_check_digit with non-numeric characters.
        """
        check_digit = self.processor.calculate_check_digit("ABCD1234")
        self.assertEqual(check_digit, '0')  # Expected check digit is '0'

    def test_encode_mrz_with_different_data(self):
        """
        Test encode_mrz with different input data.
        """
        data = {
            "Document Type": "P",
            "Issuing Country": "UTO",
            "Name": "DOE<<JANE<ELIZABETH",
            "Passport Number": "L898902C3",
            "Nationality": "UTO",
            "Date of Birth": "740812",
            "Gender": "F",
            "Expiration Date": "120415",
            "Personal Number": "ZE184226B"
        }
        line1, line2 = self.processor.encode_mrz(data)
        self.assertTrue(line1.startswith("P<UTODOE"))
        self.assertTrue(line2.startswith("L898902C3"))

    def test_decode_mrz_invalid_format(self):
        """
        Test decode_mrz with invalid MRZ format to trigger exception handling.
        """
        self.processor.scan_mrz("INVALID_LINE1", "INVALID_LINE2")
        result = self.processor.decode_mrz()
        self.assertEqual(result, "Error: Invalid MRZ data format.")

    def test_decode_mrz_with_only_line1(self):
        """
        Test decode_mrz when only line1 is provided.
        """
        self.processor.scan_mrz("P<TJKCOMBS<<ADDISON<JANE<<<<<<<<<<<<<<<<<<<<", "")
        result = self.processor.decode_mrz()
        self.assertEqual(result, "Error: MRZ data is missing.")

    def test_calculate_check_digit_empty_string(self):
        """
        Test calculate_check_digit with an empty string.
        """
        check_digit = self.processor.calculate_check_digit("")
        self.assertEqual(check_digit, '0')

if __name__ == '__main__':
    unittest.main()
