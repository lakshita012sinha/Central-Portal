from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'application_code',
        'application_name',
        'status',
        'version',
        'display_order',
        'created_at',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'application_code',
        'application_name',
    )

    ordering = (
        'display_order',
        'application_name',
    )