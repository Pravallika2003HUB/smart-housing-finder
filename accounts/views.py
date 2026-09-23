from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from favourites.models import Favourite
from properties.models import Property
from reports.models import Report
from reviews.models import Review

from .forms import ProfileForm, RegisterForm
from .models import User


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Smart Housing Finder!")
            return redirect("accounts:dashboard")
        messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.is_platform_admin:
        context = {
            "total_users": User.objects.count(),
            "students": User.objects.filter(role=User.STUDENT).count(),
            "owners": User.objects.filter(role=User.OWNER).count(),
            "properties": Property.objects.count(),
            "verified": Property.objects.filter(is_verified=True).count(),
            "pending": Property.objects.filter(is_verified=False).count(),
            "reviews": Review.objects.count(),
            "pending_reports": Report.objects.filter(status=Report.PENDING).count(),
            "listings": Property.objects.select_related("owner").order_by("-created_at")[:50],
            "reports": Report.objects.select_related("property", "user").order_by("-created_at")[:50],
        }
        return render(request, "dashboard/admin.html", context)

    if user.is_owner:
        listings = (
            Property.objects.filter(owner=user)
            .annotate(review_total=Count("reviews"), avg_rating=Avg("reviews__rating"))
            .order_by("-created_at")
        )
        context = {
            "listings": listings,
            "total": listings.count(),
            "verified": listings.filter(is_verified=True).count(),
            "pending": listings.filter(is_verified=False).count(),
            "reviews": Review.objects.filter(property__owner=user).count(),
            "reports": Report.objects.filter(property__owner=user).select_related("property"),
        }
        return render(request, "dashboard/owner.html", context)

    context = {
        "favourites": Favourite.objects.filter(user=user).select_related("property"),
        "reviews": Review.objects.filter(user=user).select_related("property"),
        "reports": Report.objects.filter(user=user).select_related("property"),
        "recommended": Property.objects.filter(is_active=True, is_verified=True).order_by("-created_at")[:6],
    }
    return render(request, "dashboard/student.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
