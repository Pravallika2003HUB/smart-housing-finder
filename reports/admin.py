from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("property", "user", "reason", "status", "created_at")
    list_filter = ("status", "reason")
    search_fields = ("property__title", "user__email")
