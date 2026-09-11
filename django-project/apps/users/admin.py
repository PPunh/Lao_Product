# coding=utf-8
from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models
from . import forms


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    model = models.User

    def display_modified(self, obj):  # display modified in local time
        if obj.date_modified:
            return timezone.localtime(obj.date_modified).strftime('%Y-%m-%d %H:%M')
        return "-"

    display_modified.short_description = "Modified"  # Set the column header

    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'phone_number', 'display_modified', 'modified_by'
    )

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            'Extra Info', {
                    'fields': (
                        'phone_number',
                        'modified_by'
                        )
                }
            ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('phone_number',)}),
    )
