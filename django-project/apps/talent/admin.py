from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import TalentApplication, TalentOpportunity, TalentProfile


@admin.register(TalentProfile)
class TalentProfileAdmin(TabbedTranslationAdmin):
    list_display = ('owner', 'headline', 'availability', 'is_active')
    list_filter = ('availability', 'is_active')
    search_fields = ('owner__username', 'owner__email', 'headline', 'skills')


@admin.register(TalentOpportunity)
class TalentOpportunityAdmin(TabbedTranslationAdmin):
    list_display = ('code', 'title', 'organization_name', 'opportunity_type', 'status', 'deadline')
    list_filter = ('opportunity_type', 'status')
    search_fields = ('code', 'title', 'organization_name')
    readonly_fields = ('code', 'created_at', 'updated_at', 'created_by', 'updated_by')


@admin.register(TalentApplication)
class TalentApplicationAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'talent', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('opportunity__title', 'talent__headline', 'talent__owner__username')