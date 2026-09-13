from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter

def money_format(value, decimals=2):
    """Format money with comma grouping regardless of the active locale."""
    if value in (None, ''):
        return ''

    try:
        decimal_value = Decimal(str(value))
        decimal_places = int(decimals)
    except (InvalidOperation, TypeError, ValueError):
        return value

    return f'{decimal_value:,.{decimal_places}f}'
