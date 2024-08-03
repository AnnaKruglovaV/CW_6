from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number_views', 'created_at')
    list_filter = ('number_views', 'created_at')
    search_fields = ('title', "content",)
