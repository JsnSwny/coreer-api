# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Language(models.Model):
    CATEGORY_TYPES = (
        ('L', 'Language'),
        ('F', 'Framework'),
        ('O', 'Other')
    )

    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=1, choices=CATEGORY_TYPES, default="O")
    icon_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} -> {self.icon_name}"
    
class Interest(models.Model):
    INTEREST_TYPES = (
        ('C', 'Career'),
        ('P', 'Personal'),
    )

    name = models.CharField(max_length=255, unique=True)
    interest_type = models.CharField(max_length=1, choices=INTEREST_TYPES)

    def __str__(self):
        return f"{self.name}"
    
class CareerLevel(models.Model):
    INTEREST_TYPES = (
        ('S', 'Student'),
        ('P', 'Professional')
    )

    name = models.CharField(max_length=20)
    level_type = models.CharField(max_length=1, choices=INTEREST_TYPES)
    def __str__(self):
        return self.name


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

class Question(models.Model):
    QUESTION_TYPES = (
        ('S', 'Student'),
        ('P', 'Professional'),
        ('R', 'Project')
    )
    text = models.TextField()
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPES)

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
    bio = models.CharField(max_length=500, default="", blank=True, null=True)
    job = models.CharField(max_length=500, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=500, blank=True, null=True)
    profile_photo = models.CharField(max_length=500, blank=True, null=True)
    languages = models.ManyToManyField(Language)
    interests = models.ManyToManyField(Interest)
    current_level = models.ForeignKey(CareerLevel, on_delete=models.CASCADE, related_name="current_level_users", null=True, blank=True)
    looking_for = models.ManyToManyField(CareerLevel, related_name="looking_for_users", null=True, blank=True)
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
    
class UserAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    
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
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    video = models.FileField(upload_to="project_videos", null=True, blank=True)
    user = models.ForeignKey(CustomUser, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    languages = models.ManyToManyField(Language, null=True, blank=True)
    repo_link = models.URLField(max_length=200, null=True, blank=True)
    project_link = models.URLField(max_length=200, null=True, blank=True)
    video_link = models.URLField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = models.ImageField(upload_to='uploads/',
                              verbose_name='Image')

class ProjectAnswer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.id} -> {self.following.id}"
    






    
