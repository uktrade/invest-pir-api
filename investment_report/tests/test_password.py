from investment_report.password_validation import (
    PIRPasswordValidator, UPPER_CASE, LOWER_CASE,
    ONE_DIGIT, MIN_LENGTH, SPECIAL_CHAR
)

from django.core.exceptions import ValidationError
from django.test import TestCase


class PasswordValidatorTestCase(TestCase):
    def test_password_validation(self):
        validator = PIRPasswordValidator()

        with self.assertRaises(ValidationError) as context:
            validator.validate('')

        self.assertTrue(UPPER_CASE in context.exception.code)
        self.assertTrue(LOWER_CASE in context.exception.code)
        self.assertTrue(ONE_DIGIT in context.exception.code)
        self.assertTrue(MIN_LENGTH in context.exception.code)
        self.assertTrue(SPECIAL_CHAR in context.exception.code)

        with self.assertRaises(ValidationError) as context:
            validator.validate('1aA!')

        self.assertFalse(UPPER_CASE in context.exception.code)
        self.assertFalse(LOWER_CASE in context.exception.code)
        self.assertFalse(ONE_DIGIT in context.exception.code)
        self.assertFalse(SPECIAL_CHAR in context.exception.code)
        # Still too short
        self.assertTrue(MIN_LENGTH in context.exception.code)

        try:
            validator.validate('1aAaaaaaaaaaaa!')
        except ValidationError:
            self.fail('Validator expectedly rejected password')
