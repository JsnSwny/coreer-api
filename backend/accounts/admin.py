# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Follow, Language, Interest, Project

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'first_name', 'last_name', 'email', 'bio', 'type', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'bio', 'tfidf_input', 'type', 'languages', 'interests', 'job', 'lat', 'lon', 'location', 'profile_photo', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'bio', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
admin.site.register(Language)
admin.site.register(Interest)
admin.site.register(Project)