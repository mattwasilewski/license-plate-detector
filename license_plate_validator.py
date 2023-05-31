import re

class LicensePlateValidator:
    def validate_license_plate(self, text):
        pattern = r'^[A-Z]{2}\s?\d{2,3}[A-Z0-9]{1,2}$'
        if re.match(pattern, text):
            return True
        else:
            return False