# chat/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='startswith')
def startswith(value, arg):
    return value.startswith(arg)

@register.filter(name='without_first_char')
def without_first_char(value):
    return value[1:]
