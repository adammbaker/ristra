from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def is_valid_alien_number(entry):
    valid_alien_number_length = (7,8,9)
    if entry.upper().startswith('A'):
        if len(entry[1:]) not in valid_alien_number_length:
            raise ValidationError(
                _('The alien number is incorrectly formatted; it should start with a capital A and be followed by 7 to 9 digits'),
            )
    else:
        raise ValidationError(
            _('The alien number is incorrectly formatted; it should start with a capital A and be followed by 7 to 9 digits'),
        )
