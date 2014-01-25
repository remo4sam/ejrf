from django import template

register = template.Library()

@register.filter
def display_list(_list):
    new_list = [str(item) for item in _list]
    return ', '.join(new_list)