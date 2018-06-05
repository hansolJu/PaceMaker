from django import template

register = template.Library()


@register.filter
def re_name(value):
    value = value[:1] + "**"
    return value