from django import template

register = template.Library()


@register.filter
def model_name(obj_item):
    """Шаблонный фильтр model_name"""
    try:
        return obj_item._meta.model_name
    except AttributeError:
        return None
