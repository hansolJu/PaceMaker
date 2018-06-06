from django import template

register = template.Library()


@register.filter
def index(List, i):
    return List[int(i)]


@register.filter()
def to_int(value):
    return int(value)


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def change_semester(value):
    if value == 0:
        return "1학년 1학기"
    elif value == 1:
        return "1학년 2학기"
    elif value == 2:
        return "2학년 1학기"
    elif value == 3:
        return "2학년 2학기"
    elif value == 4:
        return "3학년 1학기"
    elif value == 5:
        return "3학년 2학기"
    elif value == 6:
        return "4학년 1학기"
    elif value == 7:
        return "4학년 2학기"
