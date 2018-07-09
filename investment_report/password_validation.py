import re

from django.core.exceptions import ValidationError


UPPER_CASE = 'upper_case'
LOWER_CASE = 'lower_case'
ONE_DIGIT = 'one_digit'
MIN_LENGTH = 'min_length'
SPECIAL_CHAR = 'special_char'


class PIRPasswordValidator:
    def __init__(self, *args, **kwargs):
        self.rules = {
            ('contain at least one uppercase character', UPPER_CASE): (
                lambda s: any(x.isupper() for x in s)
            ),
            ('have at least one lowercase character', LOWER_CASE): (
                lambda s: any(x.islower() for x in s)
            ),
            ('have at least one digit', ONE_DIGIT): (
                lambda s: any(x.isdigit() for x in s)
            ),
            ('be at least 8 characters', MIN_LENGTH): (
                lambda s: len(s) >= 7
            ),
            ('have a special character', SPECIAL_CHAR): (
                lambda s: len(re.findall('[^a-zA-Z\d\s:]', s)) > 0
            )
        }

    def validate(self, password, user=None):
        errors = []
        error_codes = []

        for (msg, code), rule in self.rules.items():
            if not rule(password):
                errors.append(msg)
                error_codes.append(code)

        if errors:
            raise ValidationError(
                "Your password must: {}.".format('; '.join(errors)),
                code=','.join(error_codes)
            )

    def get_help_text(self):
        return "Your password must {}".format('; '.join(self.rules.keys()))
