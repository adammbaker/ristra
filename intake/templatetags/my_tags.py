from django import template
from django.utils import timezone

from datetime import timedelta

# Create your filters here.
register = template.Library()

@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural

@register.filter
def shorten(obj, length=100):
    if len(obj) == 0:
        return obj
    if len(obj) <= length:
        return obj
    if obj[:length].endswith((' ', ',',)):
        return obj[:length - 1].strip() + '…'
    return ' '.join(obj[:length].split()[:-1]) + '…'

@register.filter
def to_phone_number(number, callable=False):
    'Convert a 10 character string into (xxx) xxx-xxxx'
    if number.startswith('+1'):
        number = number[2:].strip()
    number = [x for x in number if x.isdigit()]
    if len(number) == 10:
        first = ''.join(number[0:3])
        second = ''.join(number[3:6])
        third = ''.join(number[6:10])
        if callable:
            return f'{first}-{second}-{third}'
        return f'({first}) {second}-{third}'
    return number

@register.filter
def time_to_now(obj, as_string=False):
    'Returns a timedelta obj, or human-readable version if True'
    if isinstance(obj, timedelta):
        td = obj
    else:
        td = obj - timezone.now()
    if as_string:
        string = ''
        if td.days:
            string += f'{td.days}d '
        remaining_seconds = td.seconds % 86400
        hours = remaining_seconds // 3600 
        # remaining seconds
        remaining_seconds -= hours * 3600
        # minutes
        minutes = remaining_seconds // 60
        # remaining seconds
        seconds = remaining_seconds - (minutes * 60)
        # total time
        string += f'{hours}h {minutes}m'
        return string
    return td