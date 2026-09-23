from django.conf import settings
from django.db import models

from properties.models import Property


class Favourite(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favourites")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favourites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("property", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} saved {self.property}"
