from django import template
from django.utils import timezone

from datetime import datetime, timedelta

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
    number_copy = [x for x in number if x.isdigit()]
    if len(number_copy) == 10:
        first = ''.join(number_copy[0:3])
        second = ''.join(number_copy[3:6])
        third = ''.join(number_copy[6:10])
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
    try:
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
    except TypeError:
        return obj

@register.filter
def time_to_now_abs(obj, as_string=False):
    'Returns a timedelta obj, or human-readable version if True'
    try:
        if isinstance(obj, timedelta):
            td = obj
        else:
            if timezone.now() > obj:
                td = timezone.now() - obj
            elif timezone.now() <= obj:
                td = obj - timezone.now()
        if as_string:
            string = ''
            if td.days:
                string += f'{abs(td.days)}d '
            remaining_seconds = td.seconds % 86400
            hours = remaining_seconds // 3600 
            # remaining seconds
            remaining_seconds -= hours * 3600
            # minutes
            minutes = remaining_seconds // 60
            # remaining seconds
            seconds = remaining_seconds - (minutes * 60)
            # total time
            string += f'{hours:02d}h {minutes:02d}m'
            return string
        return td
    except TypeError:
        return obj

@register.filter
def hdYIMp(obj):
    'Takes a datetime object and returns it in mm dd YYYY II:MM p'
    if isinstance(obj, datetime):
        return obj.strftime('%h %d, %Y %I:%M %p')
    return obj

@register.filter
def mdYIMp(obj):
    'Takes a datetime object and returns it in mm/dd/YYYY II:MM p'
    if isinstance(obj, datetime):
        return obj.strftime('%m/%d/%Y %I:%M %p')
    return obj


@register.filter
def add_fortnight(obj):
    'Takes a datetime object and adds 2 weeks (COVID)'
    if isinstance(obj, datetime):
        return obj + timedelta(14)
    return obj


@register.filter
def divided_by(obj, num):
    'Divides a number another number'
    if isinstance(obj, int):
        return obj // num
    return obj


@register.filter
def dec_places(obj, dec_places):
    'Divides a number another number'
    if isinstance(obj, float):
        return f'{obj:.2f}'
    return obj