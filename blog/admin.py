from django.contrib import admin
from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'pub_date', 'category')  # Отображение полей в списке
    list_filter = ('is_published', 'pub_date', 'category')  # Фильтры для удобства
    search_fields = ('title', 'text', 'author__username')  # Поиск по заголовку, тексту и автору
    list_editable = ('is_published',)  # Поле is_published можно редактировать прямо в списке
    prepopulated_fields = {'title': ('title',)}  # Автоматическое заполнение заголовка
    date_hierarchy = 'pub_date'  # Навигация по дате


admin.site.register(Post, PostAdmin)
