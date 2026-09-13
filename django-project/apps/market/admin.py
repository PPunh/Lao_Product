from django.contrib import admin

from .models import MarketCategory, MarketUpdate


@admin.register(MarketCategory)
class MarketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MarketUpdate)
class MarketUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_published', 'published_at')
    list_filter = ('is_featured', 'is_published', 'category')
    search_fields = ('title', 'summary', 'content')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')