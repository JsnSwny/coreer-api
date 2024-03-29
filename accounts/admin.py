# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Follow, Language, Interest, Project, School, Education, Question, UserAnswer, CareerLevel, ProjectAnswer, ProjectImage

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ['first_name','last_name','id','email']
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'type', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('image', 'username', 'first_name', 'last_name', 'email', 'bio', 'tfidf_input', 'type', 'languages', 'interests', 'current_level', 'looking_for', 'job', 'lat', 'lon', 'location', 'profile_photo', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('image', 'first_name', 'last_name', 'email', 'bio', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    ordering = ('email',)

class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]
    search_fields = ['title', 'user__id']

class FollowAdmin(admin.ModelAdmin):
    autocomplete_fields = ["follower", "following"]

class EducationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]

class UserAnswerAdmin(admin.ModelAdmin):
    autocomplete_fields = ["user"]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Language)
admin.site.register(ProjectImage)
admin.site.register(Interest)
admin.site.register(CareerLevel)
admin.site.register(ProjectAnswer)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(Question)
admin.site.register(Project, ProjectAdmin)
admin.site.register(School)
admin.site.register(Education, EducationAdmin)