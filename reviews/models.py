from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from properties.models import Property


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One review per user per property - stops review spam.
        unique_together = ("property", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.property.title} - {self.rating}*"
