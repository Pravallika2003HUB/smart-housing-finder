from django.conf import settings
from django.db import models

from properties.models import Property


class Report(models.Model):
    FAKE = "Fake listing"
    WRONG = "Wrong information"
    SCAM = "Scammer"
    MISSING = "Property does not exist"
    INAPPROPRIATE = "Inappropriate content"
    OTHER = "Other"
    REASON_CHOICES = [
        (FAKE, FAKE),
        (WRONG, WRONG),
        (SCAM, SCAM),
        (MISSING, MISSING),
        (INAPPROPRIATE, INAPPROPRIATE),
        (OTHER, OTHER),
    ]

    PENDING = "Pending"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"
    STATUS_CHOICES = [
        (PENDING, PENDING),
        (INVESTIGATING, INVESTIGATING),
        (RESOLVED, RESOLVED),
        (REJECTED, REJECTED),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=40, choices=REASON_CHOICES, default=FAKE)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.property.title} - {self.reason} ({self.status})"
