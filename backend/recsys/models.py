from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Recommendation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations_from")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations_to")
    recommended_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.from_user.id} -> {self.to_user.id} ({self.recommended_on})"