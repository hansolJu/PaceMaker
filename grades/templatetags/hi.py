from django import template
register = template.Library()


@register.filter()
def to_int(value):
    return int(value)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def get_at_index(list, index):
    return list[index]