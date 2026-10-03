from django.contrib import admin

from .models import (
    SSOClient,
    SSOAuthorizationCode,
)


@admin.register(SSOClient)
class SSOClientAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'client_id',
        'environment',
        'code_expiry_seconds',
        'token_method',
        'is_active',
        'created_at',
    )

    list_filter = (
        'environment',
        'token_method',
        'is_active',
    )

    search_fields = (
        'client_id',
        'application__application_name',
        'application__application_code',
    )


@admin.register(SSOAuthorizationCode)
class SSOAuthorizationCodeAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'client',
        'user',
        'ulb',
        'expires_at',
        'used_at',
        'created_at',
    )

    list_filter = (
        'client',
        'ulb',
    )

    search_fields = (
        'user__username',
        'client__client_id',
        'ulb__ulb_code',
    )

    readonly_fields = (
        'code',
        'created_at',
    )