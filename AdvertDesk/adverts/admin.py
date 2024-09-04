from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import (Category, Advert,
                     Author, Response)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ-панель модели категорий
    """
    list_display = ('tree_actions', 'indented_title', 'id', 'name', 'slug')
    list_display_links = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Основная информация', {'fields': ('name', 'slug', 'parent')}),
        ('Описание', {'fields': ('description',)})
    )


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Response)
class ResponseAdminPage(admin.ModelAdmin):
    """
    Админ-панель модели откликов
    """
    list_display = ('advert', 'user', 'time_create', 'status')
    list_filter = ('time_create', 'time_update', 'user')
    list_editable = ('status',)


admin.site.register(Author)


# Register your models here.
