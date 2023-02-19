# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    likes = models.ManyToManyField('self', blank=True, related_name="user_likes")
    bio = models.CharField(max_length=500, default="")
    job = models.CharField(max_length=500, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    profile_photo = models.CharField(max_length=500, blank=True, null=True)




    def __str__(self):
        return self.email