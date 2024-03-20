from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.


class User(AbstractUser):
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    REQUIRED_FIELDS = ['age']
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.can_data_be_shared and self.age < 15:
            raise ValidationError(
                'User must be at least 18 years old to share data.')
        super().save(*args, **kwargs)
