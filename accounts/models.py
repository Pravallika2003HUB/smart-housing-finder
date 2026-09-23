from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user with a role and phone number. Passwords are hashed by Django."""

    STUDENT = "student"
    OWNER = "owner"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (STUDENT, "Student / Bachelor"),
        (OWNER, "Property Owner"),
        (ADMIN, "Admin"),
    ]

    email = models.EmailField("email address", unique=True)
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_owner(self):
        return self.role == self.OWNER

    @property
    def is_student(self):
        return self.role == self.STUDENT

    @property
    def is_platform_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.full_name or self.username} ({self.role})"
