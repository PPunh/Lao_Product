# coding=utf-8
from django.urls import reverse, resolve, NoReverseMatch, Resolver404
from django import template
from django.template.defaultfilters import floatformat
from decimal import Decimal
from django.utils import translation
from django.urls import translate_url

register = template.Library()

@register.filter
def get_obj_attr(obj, attr_path):
    """
    Get attribute from object by path like 'product.name' or 'product__name
    """
    try:
        # Change __ to . for nested attribute
        # Example: product__name -> product.name
        path = attr_path.replace('__', '.')
        for part in path.split('.'):
            obj = getattr(obj, part)
        return obj
    except (AttributeError, TypeError):
        return ""

@register.filter
def percentage(value, total):
    """Calculate percentage of value out of total"""
    try:
        if total and total != 0:
            return (Decimal(str(value)) / Decimal(str(total)) * Decimal('100'))
        return Decimal('0')
    except (ValueError, TypeError, ZeroDivisionError):
        return Decimal('0')

@register.filter
def percentage_format(value, total):
    """Format as percentage with 2 decimal places"""
    try:
        if total and total != 0:
            result = (Decimal(str(value)) / Decimal(str(total)) * Decimal('100'))
            return floatformat(result, '2')
        return "0.00"
    except (ValueError, TypeError, ZeroDivisionError):
        return "0.00"

@register.filter
def multiply(value, arg):
    """Multiply value by argument"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return Decimal('0')

@register.filter
def divide(value, arg):
    """Divide value by argument"""
    try:
        if arg and arg != 0:
            return Decimal(str(value)) / Decimal(str(arg))
        return Decimal('0')
    except (ValueError, TypeError, ZeroDivisionError):
        return Decimal('0')

@register.filter
def subtract(value, arg):
    """Subtract argument from value"""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except (ValueError, TypeError):
        return Decimal('0')


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    request = context.get('request')
    if not request:
        return ''

    path = request.path

    try:
        url_paths = resolve(path)

        view_kwargs = url_paths.kwargs.copy()
        view_kwargs.pop('lang_code', None)
        view_kwargs.pop('language', None)

        with translation.override(lang):
            new_url = reverse(
                url_paths.view_name,
                args=url_paths.args,
                kwargs=view_kwargs
            )

        if request.GET:
            query_string = request.GET.urlencode()
            new_url = f"{new_url}?{query_string}"

        return new_url

    except (NoReverseMatch, Resolver404):
        return translate_url(path, lang)
