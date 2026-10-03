from django.conf import settings
from django.db import models

from applications.models import Application
from ulbs.models import ULB


class Role(models.Model):

    ROLE_TYPE_CHOICES = [
        ('SYSTEM', 'System'),
        ('ULB', 'ULB'),
        ('APPLICATION', 'Application'),
    ]

    role_name = models.CharField(
        max_length=100
    )

    role_code = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    role_type = models.CharField(
        max_length=20,
        choices=ROLE_TYPE_CHOICES,
        default='APPLICATION'
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='roles',
        blank=True,
        null=True
    )

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='roles',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.role_name

class Permission(models.Model):

    permission_name = models.CharField(
        max_length=100
    )

    permission_code = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.permission_name

class RolePermission(models.Model):

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_permissions'
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='role_permissions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'permission'],
                name='unique_role_permission'
            )
        ]

    def __str__(self):
        return f"{self.role.role_name} - {self.permission.permission_name}"

class ULBApplicationAccess(models.Model):

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='application_access'
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='ulb_access'
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ulb', 'application'],
                name='unique_ulb_application_access'
            )
        ]

    def __str__(self):
        return (
            f"{self.ulb.ulb_name} - "
            f"{self.application.application_name}"
        )
class UserApplicationAccess(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='application_access'
    )

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='user_application_access'
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='user_access'
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name='user_application_access',
        blank=True,
        null=True
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'ulb', 'application'],
                name='unique_user_ulb_application_access'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.ulb.ulb_name} - "
            f"{self.application.application_name}"
        )            