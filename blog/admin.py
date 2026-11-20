from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'author',
        'status',
        'view_count',
        'created_at',
    )
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at', 'view_count')
