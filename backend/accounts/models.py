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
    


class School(models.Model):
    logo = models.ImageField(upload_to="logos", blank=True, null=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        if self.logo:
            return f"{self.id} {self.name} - Has Logo"
        else:
            return f"{self.id} {self.name}"

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    STUDENT = 'Student'
    PROFESSIONAL = 'Professional'
    TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSIONAL, 'Professional'),
    ]

    # username = models.CharField(max_length=150, unique=True)

    image = models.ImageField(upload_to='profiles/', default='profiles/default-image.png')
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
    onboarded = models.BooleanField(default=False)

    objects = CustomUserManager()

    def add_language(self, language_name):
        language, created = Language.objects.get_or_create(name=language_name)
        self.languages.add(language)
        return created
    
    def __str__(self):
        return self.email
    
class Education(models.Model):
    user = models.ForeignKey(CustomUser, related_name='educations', on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey(School, related_name='educations', on_delete=models.CASCADE, null=True, blank=True)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

class WorkExperience(models.Model):
    user = models.ForeignKey(CustomUser, related_name='work_experiences', on_delete=models.CASCADE, null=True, blank=True)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
class Project(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True)
    video = models.FileField(upload_to="project_videos", null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    languages = models.ManyToManyField(Language, null=True, blank=True)
    content = models.TextField()
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.id} -> {self.following.id}"
    






    
