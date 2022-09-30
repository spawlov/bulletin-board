from django import template

register = template.Library()


@register.filter()
def attach_name(in_text):
    return str(in_text).split('/')[-1]
