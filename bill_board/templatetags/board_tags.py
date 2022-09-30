from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
# Сохранение исходного URL для корректной работы пагинации
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
