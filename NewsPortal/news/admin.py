from django.contrib import admin
from .models import (Category, Post, PostCategory,
                     Author, Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'post_time_in', 'post_type', 'author', 'category')
    list_filter = ('post_time_in', 'post_type', 'author')
    search_fields = ('title', 'post_time_in', 'post_type', 'author__user__username', 'categories__name')

    def category(self, obj):
        return "\n".join([p.name for p in obj.categories.all()])


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)

# Register your models here.
