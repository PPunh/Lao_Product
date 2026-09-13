# coding=utf-8
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
        HeroModel,
    )


@admin.register(HeroModel)
class HeroAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'order')
    search_fields = ('title', )
    list_filter = ('is_active', )