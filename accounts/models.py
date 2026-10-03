from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    force_password_change = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username