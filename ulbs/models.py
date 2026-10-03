from django.db import models
from django.conf import settings
from applications.models import Application

class ULB(models.Model):

    ULB_TYPE_CHOICES = [
        ('MUNICIPAL_CORPORATION', 'Municipal Corporation'),
        ('MUNICIPAL_COUNCIL', 'Municipal Council'),
        ('MUNICIPALITY', 'Municipality'),
        ('NAGAR_PANCHAYAT', 'Nagar Panchayat'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    ulb_code = models.CharField(
        max_length=50,
        unique=True
    )

    ulb_name = models.CharField(
        max_length=255
    )

    ulb_type = models.CharField(
        max_length=50,
        choices=ULB_TYPE_CHOICES
    )

    state = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    legal_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    valid_from = models.DateField()

    valid_to = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    is_active = models.BooleanField(
        default=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.ulb_code} - {self.ulb_name}"

class ULBDatabaseConfiguration(models.Model):

    DATABASE_ENGINE_CHOICES = [
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='database_configurations'
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='ulb_database_configurations'
    )

    database_alias = models.CharField(
        max_length=100,
        unique=True
    )

    database_name = models.CharField(
        max_length=255
    )

    database_host = models.CharField(
        max_length=255
    )

    database_port = models.PositiveIntegerField(
        default=5432
    )

    database_username = models.CharField(
        max_length=255
    )

    database_secret_reference = models.CharField(
        max_length=255
    )

    database_engine = models.CharField(
        max_length=50,
        choices=DATABASE_ENGINE_CHOICES,
        default='postgresql'
    )

    ssl_required = models.BooleanField(
        default=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
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
                name='unique_ulb_application_database'
            )
        ]

    def __str__(self):
        return (
            f"{self.ulb.ulb_name} - "
            f"{self.application.application_name}"
        )

class ULBMembership(models.Model):

    USER_TYPE_CHOICES = [
        ('ULB_ADMIN', 'ULB Admin'),
        ('END_USER', 'End User'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ulb_memberships'
    )

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
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
                fields=['user', 'ulb'],
                name='unique_user_ulb_membership'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.ulb.ulb_name}"    

class ULBApplication(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    ulb = models.ForeignKey(
        ULB,
        on_delete=models.CASCADE,
        related_name='application_grants'
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='ulb_grants'
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    default_role = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    configuration_override = models.JSONField(
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
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
                name='unique_ulb_application'
            )
        ]

    def __str__(self):
        return f"{self.ulb.ulb_name} - {self.application.application_name}"    