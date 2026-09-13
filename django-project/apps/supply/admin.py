from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import SupplierProfile, SupplyListing


@admin.register(SupplierProfile)
class SupplierProfileAdmin(TabbedTranslationAdmin):
    list_display = ('business_name', 'owner', 'is_verified', 'is_active')
    list_filter = ('is_verified', 'is_active')
    search_fields = ('business_name', 'owner__username', 'owner__email')


@admin.register(SupplyListing)
class SupplyListingAdmin(TabbedTranslationAdmin):
    list_display = ('code', 'title', 'supplier', 'listing_type', 'status', 'is_active')
    list_filter = ('listing_type', 'status', 'is_active')
    search_fields = ('code', 'title', 'supplier__business_name')
    readonly_fields = ('code', 'created_at', 'updated_at', 'created_by', 'updated_by')