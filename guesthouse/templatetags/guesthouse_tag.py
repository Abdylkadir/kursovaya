from django import template
from guesthouse.models import Category, Location


register = template.Library()  # Для регистрации темплейт тегов


@register.simple_tag()  # Декораттор,который зарегестрирует темплейт тег
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('guesthouse/tags/last_location.html')
def get_last_locations(count=5):
    locations = Location.objects.order_by("id")[:count]
    return {"last_locations": locations}
