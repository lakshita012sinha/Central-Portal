from django.contrib import admin

from .models import (
    Role,
    Permission,
    RolePermission,
    UserApplicationAccess,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = (
        'role_name',
        'role_code',
        'role_type',
        'application',
        'ulb',
        'is_active',
        'created_at',
    )

    list_filter = (
        'role_type',
        'is_active',
        'application',
        'ulb',
    )

    search_fields = (
        'role_name',
        'role_code',
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = (
        'permission_name',
        'permission_code',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'permission_name',
        'permission_code',
    )


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):

    list_display = (
        'role',
        'permission',
        'created_at',
    )

    list_filter = (
        'role',
        'permission',
    )

    search_fields = (
        'role__role_name',
        'permission__permission_name',
    )


@admin.register(UserApplicationAccess)
class UserApplicationAccessAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'ulb',
        'application',
        'role',
        'start_date',
        'end_date',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'ulb',
        'application',
        'role',
    )

    search_fields = (
        'user__username',
        'user__email',
        'ulb__ulb_name',
        'ulb__ulb_code',
        'application__application_name',
        'application__application_code',
        'role__role_name',
    )