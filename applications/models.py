from django.db import models


class Application(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    application_code = models.CharField(
        max_length=50,
        unique=True
    )

    application_name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    icon = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    base_url = models.URLField(
        max_length=500
    )

    launch_url = models.URLField(
        max_length=500
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    version = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.application_code} - {self.application_name}"