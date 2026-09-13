# coding=utf-8
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import DemandCenterModel, NewsModel

@admin.register(NewsModel)
class NewsAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'subject', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'subject', 'content')
    ordering = ('-created_at',)


@admin.register(DemandCenterModel)
class DemandCenterAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'contact_number', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'contact_number', 'email')
    ordering = ('name',)