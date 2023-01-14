# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    likes = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username