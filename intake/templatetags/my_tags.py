from django import template

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
    if obj[:length].endswith((' ', ',',)):
        return obj[:length - 1].strip() + '…'
    return ' '.join(obj[:length].split()[:-1]) + '…'