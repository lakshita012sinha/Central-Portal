from django.db import models

from applications.models import Application
import uuid
from accounts.models import User
from ulbs.models import ULB

class SSOClient(models.Model):

    ENVIRONMENT_CHOICES = [
        ('DEVELOPMENT', 'Development'),
        ('STAGING', 'Staging'),
        ('PRODUCTION', 'Production'),
    ]

    TOKEN_METHOD_CHOICES = [
        ('CLIENT_SECRET_POST', 'Client Secret Post'),
        ('CLIENT_SECRET_BASIC', 'Client Secret Basic'),
    ]

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='sso_client'
    )

    client_id = models.CharField(
        max_length=255,
        unique=True
    )

    client_secret = models.CharField(
        max_length=500
    )

    audience = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    issuer = models.URLField(
        max_length=500
    )

    allowed_redirect_uri = models.URLField(
        max_length=500
    )

    code_expiry_seconds = models.PositiveIntegerField(
        default=60
    )

    environment = models.CharField(
        max_length=20,
        choices=ENVIRONMENT_CHOICES,
        default='DEVELOPMENT'
    )

    token_method = models.CharField(
        max_length=30,
        choices=TOKEN_METHOD_CHOICES,
        default='CLIENT_SECRET_BASIC'
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
        return f"{self.application.application_name} - {self.client_id}"


class SSOAuthorizationCode(models.Model):

    code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    client = models.ForeignKey(
        SSOClient,
        on_delete=models.CASCADE,
        related_name='authorization_codes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sso_authorization_codes'
    )

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='sso_authorization_codes'
    )

    redirect_uri = models.URLField(
        max_length=500
    )

    expires_at = models.DateTimeField()

    used_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.code)    