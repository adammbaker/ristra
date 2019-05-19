from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def does_not_contain_commas(entry):
    if ',' in entry:
        raise ValidationError(
            _('Your entry cannot contain commas; only one email per entry is allowed'),
        )
