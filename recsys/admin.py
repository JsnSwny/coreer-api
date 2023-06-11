from django.contrib import admin
from .models import Recommendation

class RecommendationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["from_user", "to_user"]

admin.site.register(Recommendation, RecommendationAdmin)