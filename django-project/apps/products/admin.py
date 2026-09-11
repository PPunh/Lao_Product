# coding=utf-8
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
    ProductsCategoryModel,
    ProductsUnitModel,
    CurrencyModel,
    ProductsModel,
    StocksModel
)
@admin.register(CurrencyModel)
class CurrencyAdmin(TabbedTranslationAdmin):
    fields = ('code', 'currency_name', 'symbol')

@admin.register(StocksModel)
class StocksAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']

@admin.register(ProductsCategoryModel)
class ProductsCategoryModelAdmin(TabbedTranslationAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(ProductsUnitModel)
class ProductsUnitModelAdmin(TabbedTranslationAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(ProductsModel)
class ProductsModelAdmin(TabbedTranslationAdmin):
    list_display = ['code', 'name', 'category', 'unit']
    search_fields = ['code', 'name']
    list_filter = ['category', 'unit']
    ordering = ['name']
    readonly_fields = ['code', 'created_at', 'updated_at', 'created_by', 'updated_by']

    fieldsets = (
        ('Basic Information', {
            'fields': ('product_img', 'name', 'description', 'category', 'unit', 'currency', 'price', 'is_sellable')
        }),
        ('Audit Information', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
