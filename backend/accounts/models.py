# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} -> {self.icon_name}"
    
class Interest(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class CustomUser(AbstractUser):
    STUDENT = 'Student'
    PROFESSIONAL = 'Professional'
    TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSIONAL, 'Professional'),
    ]
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
    interests = models.ManyToManyField(Interest)
    tfidf_input = models.CharField(max_length=1000, default="")
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default="Student")

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
    
class Project(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True)
    user = models.ForeignKey(CustomUser, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255)
    languages = models.ManyToManyField(Language)

class School(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

class Education(models.Model):
    school = models.ManyToManyField(School)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)





    
