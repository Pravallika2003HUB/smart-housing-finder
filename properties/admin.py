from django.contrib import admin

from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "property_type", "monthly_rent", "is_verified", "is_active")
    list_filter = ("property_type", "is_verified", "is_active", "gender_preference")
    search_fields = ("title", "location", "address")
    actions = ["verify_listings", "reject_listings"]

    @admin.action(description="Verify selected listings")
    def verify_listings(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected listings as pending")
    def reject_listings(self, request, queryset):
        queryset.update(is_verified=False)
