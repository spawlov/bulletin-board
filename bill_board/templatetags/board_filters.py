from django import template

register = template.Library()


@register.filter()
# Обрезаем от имени файла путь
def attach_name(in_text):
    return str(in_text).split('/')[-1]
