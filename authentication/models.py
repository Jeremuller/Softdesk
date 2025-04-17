from django.db import models

from django.contrib.auth.models import AbstractUser


# Ceci est un test.
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    can_data_be_shared = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)

    def __str__(self):
        return self.username