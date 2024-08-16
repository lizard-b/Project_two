from django.contrib import admin
from .models import (Category, Post, PostCategory,
                     Author, Comment)
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Post
    list_display = ('title', 'preview', 'post_time_in', 'post_type', 'author', 'category')
    list_filter = ('post_time_in', 'post_type', 'author')
    search_fields = ('title', 'post_time_in', 'post_type', 'author__user__username', 'categories__name')

    def category(self, obj):
        return "\n".join([p.name for p in obj.categories.all()])


class CategoryAdmin(TranslationAdmin, admin.ModelAdmin):
    model = Category
    list_display = ('name', 'subscriber')
    list_filter = ('name', 'subscribers')
    search_fields = ('name', 'subscribers__username')

    def subscriber(self, obj):
        return ",\n".join([p.username for p in obj.subscribers.all()])


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'post'[:50])
    list_filter = ('category', )
    search_fields = ('category', 'post')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_rating')
    list_filter = ('user', 'user_rating')
    search_fields = ('user__username', 'user_rating')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'comm_time_in', 'comment_rating', 'user',)
    list_filter = ('comm_time_in', 'comment_rating', 'user',)
    search_fields = ('user__username', 'comm_time_in', 'comment_rating', 'post__title')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)

# Register your models here.
