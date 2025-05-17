from django.db import models

from django.contrib.auth.models import AbstractUser
from .validators import validate_age


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(validators=[validate_age])
    can_data_be_shared = models.BooleanField(default=False)
    can_be_contacted = models.BooleanField(default=False)

    def __str__(self):
        return self.username


