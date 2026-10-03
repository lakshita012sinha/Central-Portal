from django.contrib import admin

from .models import (
    ULB,
    ULBDatabaseConfiguration,
    ULBMembership,
    ULBApplication,
)


@admin.register(ULB)
class ULBAdmin(admin.ModelAdmin):
    list_display = (
        'ulb_code',
        'ulb_name',
        'ulb_type',
        'state',
        'district',
        'status',
        'is_active',
        'valid_from',
        'valid_to',
    )

    list_filter = (
        'status',
        'is_active',
        'ulb_type',
        'state',
    )

    search_fields = (
        'ulb_code',
        'ulb_name',
        'city',
        'district',
    )


@admin.register(ULBDatabaseConfiguration)
class ULBDatabaseConfigurationAdmin(admin.ModelAdmin):

    list_display = (
        'ulb',
        'application',
        'database_alias',
        'database_name',
        'database_host',
        'database_port',
        'database_engine',
        'ssl_required',
        'status',
    )

    list_filter = (
        'database_engine',
        'ssl_required',
        'status',
        'ulb',
        'application',
    )

    search_fields = (
        'ulb__ulb_name',
        'ulb__ulb_code',
        'application__application_name',
        'application__application_code',
        'database_alias',
        'database_name',
    )

@admin.register(ULBMembership)
class ULBMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'ulb',
        'user_type',
        'is_active',
        'created_at',
    )

    list_filter = (
        'user_type',
        'is_active',
        'ulb',
    )

    search_fields = (
        'user__username',
        'user__email',
        'ulb__ulb_name',
        'ulb__ulb_code',
    )

@admin.register(ULBApplication)
class ULBApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'ulb',
        'application',
        'start_date',
        'end_date',
        'status',
        'default_role',
        'created_at',
    )

    list_filter = (
        'status',
        'application',
        'ulb',
    )

    search_fields = (
        'ulb__ulb_name',
        'ulb__ulb_code',
        'application__application_name',
        'application__application_code',
    )    