import re
from django.core import validators

PHONE_REGEXP = '\d{10,12}'
PHONE_VALIDATORS = [validators.RegexValidator(re.compile(PHONE_REGEXP), 'Enter a valid phone.', 'invalid')]