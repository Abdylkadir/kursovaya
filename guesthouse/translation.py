from modeltranslation.translator import register, TranslationOptions
from .models import Category, Guide, Location, Genre


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Guide)
class GuideTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Location)
class LocationTranslationOptions(TranslationOptions):
    fields = ('title', 'description' )
