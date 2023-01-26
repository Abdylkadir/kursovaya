
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Location, Genre, Guide, Rating, RatingStar, Reviews


@admin.register(Category)  # Декаратор
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(Location)
class LocationAdmin(TranslationAdmin):
    """Локация"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "count")
    search_fields = ("title", "category__name")
    # save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ['publish', 'unpublish']

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Guide)
class GuideAdmin(SimpleHistoryAdmin, TranslationAdmin):
    """Гиды"""
    list_display = ("name", "description", "get_image")
    readonly_fields = ("get_image",)
    history_list_display = ["name_ru", "description_ru",]

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="50"')

    get_image.short_description = "Изображение"


@admin.register(Reviews)
class ReviewsAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'text')
    readonly_fields = ('name', 'email')
    list_display_links = ('id','email','name',)
    ordering = ('id',)
    history_list_display = ["email", "name"]


# admin.site.register(Category, CategoryAdmin)
# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin):
#     """Рейтинг"""
#     list_display = ("name", "ip")
# admin.site.register(Location)
# admin.site.register(Genre)
# admin.site.register(Guide)
# admin.site.register(LocationsShots)
admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)
