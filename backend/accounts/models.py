# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} -> {self.icon_name}"


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    bio = models.CharField(max_length=500, default="")
    job = models.CharField(max_length=500, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    profile_photo = models.CharField(max_length=500, blank=True, null=True)
    languages = models.ManyToManyField(Language)

    def add_language(self, language_name):
        language, created = Language.objects.get_or_create(name=language_name)
        self.languages.add(language)
        return created
    
    def __str__(self):
        return self.email
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.id} -> {self.following.id}"
    
