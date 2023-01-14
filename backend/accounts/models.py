# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # add additional fields in here
    likes = models.ManyToManyField('self', blank=True)
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'   
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email