from django.conf import settings
from django.db import models


class Property(models.Model):
    PG = "PG"
    HOSTEL = "Hostel"
    ROOM = "Room"
    APARTMENT = "Apartment"
    TYPE_CHOICES = [(PG, "PG"), (HOSTEL, "Hostel"), (ROOM, "Room"), (APARTMENT, "Apartment")]

    MALE = "Male"
    FEMALE = "Female"
    ANY = "Any"
    GENDER_CHOICES = [(MALE, "Male"), (FEMALE, "Female"), (ANY, "Any")]

    title = models.CharField(max_length=150)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties"
    )
    property_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=PG)
    location = models.CharField(max_length=120, db_index=True)
    address = models.TextField()
    monthly_rent = models.PositiveIntegerField()
    security_deposit = models.PositiveIntegerField(default=0)
    description = models.TextField()
    gender_preference = models.CharField(max_length=10, choices=GENDER_CHOICES, default=ANY)
    food_available = models.BooleanField(default=False)
    wifi_available = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    laundry_available = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="properties/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "properties"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def average_rating(self):
        ratings = [r.rating for r in self.reviews.all()]
        return round(sum(ratings) / len(ratings), 1) if ratings else 0

    @property
    def review_count(self):
        return self.reviews.count()
