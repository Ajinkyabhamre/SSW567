import re
import logging

# Set up logging for error reporting
logging.basicConfig(filename='mrz_errors.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# Define Damm table for checksum calculation
DAMM_TABLE = [
    [0, 3, 1, 7, 5, 9, 8, 6, 4, 2],
    [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
    [4, 2, 0, 6, 8, 7, 1, 3, 5, 9],
    [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
    [6, 1, 2, 3, 0, 4, 5, 9, 7, 8],
    [3, 6, 7, 4, 2, 0, 9, 5, 8, 1],
    [5, 8, 6, 9, 7, 2, 0, 1, 3, 4],
    [8, 9, 4, 5, 3, 6, 2, 0, 1, 7],
    [9, 4, 3, 8, 6, 1, 7, 2, 0, 5],
    [2, 5, 8, 1, 4, 3, 6, 7, 9, 0]
]

class MRZProcessor:
    def __init__(self):
        # Initialize MRZ lines
        self.line1 = ""
        self.line2 = ""

    def scan_mrz(self, line1, line2):
        """
        Simulate receiving MRZ data from a scanner.
        Accepts two strings (line1 and line2) from MRZ as inputs.
        """
        self.line1 = line1
        self.line2 = line2

    def decode_mrz(self):
        """
        Decode MRZ data and validate check digits.
        """
        if not (self.line1 and self.line2):
            logging.error("MRZ data is missing.")
            return "Error: MRZ data is missing."

        # Extract fields from MRZ lines
        try:
            # Line 1 parsing
            document_type = self.line1[0:2].replace('<', '')
            issuing_country = self.line1[2:5]
            name_field = self.line1[5:].rstrip('<')
            name = name_field.replace('<<', ' ').replace('<', ' ')
            name = ' '.join(name.split())  # Remove extra spaces

            # Line 2 parsing
            passport_number = self.line2[0:9]
            passport_check_digit = self.line2[9]
            nationality = self.line2[10:13]
            birth_date = self.line2[13:19]
            birth_check_digit = self.line2[19]
            gender = self.line2[20]
            expiration_date = self.line2[21:27]
            expiration_check_digit = self.line2[27]
            personal_number = self.line2[28:42].rstrip('<')
            final_check_digit = self.line2[42]

            # Validate check digits using Damm's algorithm
            if not self.validate_check_digit(passport_number, passport_check_digit, "passport number", 2):
                return "Check digit validation failed for passport number."
            if not self.validate_check_digit(birth_date, birth_check_digit, "birth date", 2):
                return "Check digit validation failed for birth date."
            if not self.validate_check_digit(expiration_date, expiration_check_digit, "expiration date", 2):
                return "Check digit validation failed for expiration date."

            # Combine data for final check digit
            combined_data = passport_number + birth_date + expiration_date + personal_number
            if not self.validate_check_digit(combined_data, final_check_digit, "personal number", 2):
                return "Check digit validation failed for personal number."

            # Return extracted and validated data
            return {
                "Document Type": document_type,
                "Issuing Country": issuing_country,
                "Name": name,
                "Passport Number": passport_number.strip('<'),
                "Nationality": nationality,
                "Date of Birth": birth_date,
                "Gender": gender,
                "Expiration Date": expiration_date,
                "Personal Number": personal_number,
            }
        except IndexError:
            logging.error("Invalid MRZ data format.")
            return "Error: Invalid MRZ data format."
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return "Error: An unexpected error occurred."

    def encode_mrz(self, data):
        """
        Encode fields from a simulated database retrieval into MRZ format.
        """
        # Retrieve data with default values if not provided
        document_type = data.get("Document Type", "P")
        issuing_country = data.get("Issuing Country", "UTO")
        name = data.get("Name", "DOE<<JOHN<QUINCY")
        passport_number = data.get("Passport Number", "L898902C3")
        nationality = data.get("Nationality", "UTO")
        birth_date = data.get("Date of Birth", "800101")
        gender = data.get("Gender", "M")
        expiration_date = data.get("Expiration Date", "250101")
        personal_number = data.get("Personal Number", "123456789")

        # Line 1 construction
        line1 = f"{document_type}<{issuing_country}{name:<39}".replace(" ", "<")
        line1 = line1[:44]  # Ensure line1 is 44 characters

        # Calculate check digits using Damm's algorithm
        passport_check_digit = self.calculate_check_digit(passport_number)
        birth_check_digit = self.calculate_check_digit(birth_date)
        expiration_check_digit = self.calculate_check_digit(expiration_date)

        # Format the personal number to 14 characters, padding with '<'
        personal_number_formatted = personal_number.ljust(14, '<')

        # Construct line2_partial
        line2_partial = f"{passport_number:<9}{passport_check_digit}{nationality}{birth_date}{birth_check_digit}{gender}{expiration_date}{expiration_check_digit}{personal_number_formatted}"
        line2_partial = line2_partial.replace(" ", "<")

        # Calculate the final check digit for the combined data
        combined_data = passport_number + birth_date + expiration_date + personal_number
        final_check_digit = self.calculate_check_digit(combined_data)

        # Construct line2
        line2 = f"{line2_partial}{final_check_digit}"
        line2 = line2[:44]  # Ensure line2 is 44 characters

        return line1, line2

    def validate_check_digit(self, field, check_digit, field_name, line):
        """
        Validate the check digit using Damm's algorithm.
        """
        calculated_digit = self.calculate_check_digit(field)
        if calculated_digit != check_digit:
            logging.error(f"Mismatch in {field_name} field on line {line}. Expected {calculated_digit}, got {check_digit}.")
            return False
        return True

    def calculate_check_digit(self, field):
        """
        Calculate the check digit using Damm's algorithm.
        """
        interim = 0
        for char in field:
            if char.isdigit():
                num = int(char)
                interim = DAMM_TABLE[interim][num]
            else:
                continue  # Ignore non-numeric characters
        return str(interim)

    def retrieve_from_database(self, passport_number):
        """
        Simulate retrieving data from a database using the passport number.
        """
        # Since we don't have a database, return dummy data
        dummy_data = {
            "Document Type": "P",
            "Issuing Country": "UTO",
            "Name": "DOE<<JOHN<QUINCY",
            "Passport Number": passport_number,
            "Nationality": "UTO",
            "Date of Birth": "800101",
            "Gender": "M",
            "Expiration Date": "250101",
            "Personal Number": "123456789"
        }
        return dummy_data

    def write_to_database(self, data):
        """
        Simulate writing data to a database.
        """
        # Since we don't have a database, simply pass
        pass

    def hardware_scan(self):
        """
        Simulate scanning MRZ data from a hardware device.
        """
        # Since we don't have hardware, set dummy MRZ lines
        self.line1 = "P<UTODOE<<JOHN<QUINCY<<<<<<<<<<<<<<<<<<<<<<"
        self.line2 = "L898902C36UTO8001017M2501012<<<<<<<<<<<<<<08"

# Sample usage (excluded from coverage)
if __name__ == "__main__":  # pragma: no cover
    mrz_processor = MRZProcessor()
    # Simulate scanning MRZ lines
    mrz_processor.scan_mrz(
        "P<TJKCOMBS<<ADDISON<JANE<<<<<<<<<<<<<<<<<<<<",
        "V855996J79TJK7209167M0905071MI797251T<<<<<<7"
    )
    # Decode the MRZ data
    decoded_data = mrz_processor.decode_mrz()
    print("Decoded Data:", decoded_data)
