from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AppUserAdmin(UserAdmin):
    list_display = ("email", "full_name", "role", "phone", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("email", "full_name", "phone")
    fieldsets = UserAdmin.fieldsets + (("Smart Housing", {"fields": ("full_name", "phone", "role")}),)
