from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property

from .forms import ReportForm
from .models import Report


@login_required
def add_report(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    if request.method != "POST":
        return redirect("properties:detail", pk=prop.pk)
    form = ReportForm(request.POST)
    if form.is_valid():
        report = form.save(commit=False)
        report.property = prop
        report.user = request.user
        report.status = Report.PENDING
        report.save()
        messages.success(request, "Report submitted. Our team will review it.")
    else:
        messages.error(request, "Please choose a reason for the report.")
    return redirect("properties:detail", pk=prop.pk)


@login_required
def my_reports(request):
    reports = Report.objects.filter(user=request.user).select_related("property")
    return render(request, "reports/my_reports.html", {"reports": reports})


@login_required
def update_status(request, pk, status):
    if not request.user.is_platform_admin:
        raise PermissionDenied
    report = get_object_or_404(Report, pk=pk)
    valid = dict(Report.STATUS_CHOICES)
    if status not in valid:
        messages.error(request, "Unknown status.")
    else:
        report.status = status
        report.save(update_fields=["status"])
        messages.success(request, f"Report marked {status}.")
    return redirect("accounts:dashboard")
