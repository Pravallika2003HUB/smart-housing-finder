from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from favourites.models import Favourite
from reviews.forms import ReviewForm
from reports.forms import ReportForm

from .forms import PropertyForm
from .models import Property


def home(request):
    featured = (
        Property.objects.filter(is_active=True, is_verified=True)
        .annotate(avg_rating=Avg("reviews__rating"), review_total=Count("reviews"))
        .order_by("-created_at")[:6]
    )
    return render(request, "properties/home.html", {"featured": featured})


def property_search(request):
    qs = Property.objects.filter(is_active=True).annotate(
        rating=Avg("reviews__rating"), review_total=Count("reviews")
    )
    g = request.GET
    if g.get("location"):
        qs = qs.filter(location__icontains=g["location"].strip())
    if g.get("min_rent"):
        qs = qs.filter(monthly_rent__gte=g["min_rent"])
    if g.get("max_rent"):
        qs = qs.filter(monthly_rent__lte=g["max_rent"])
    if g.get("property_type"):
        qs = qs.filter(property_type=g["property_type"])
    if g.get("gender"):
        qs = qs.filter(gender_preference=g["gender"])
    for flag in ["wifi_available", "food_available", "parking_available", "furnished"]:
        if g.get(flag):
            qs = qs.filter(**{flag: True})
    if g.get("verified_only"):
        qs = qs.filter(is_verified=True)

    sort = g.get("sort", "newest")
    qs = qs.order_by(
        {"rent_asc": "monthly_rent", "rent_desc": "-monthly_rent"}.get(sort, "-created_at")
    )
    return render(
        request,
        "properties/search.html",
        {"properties": qs, "filters": g, "types": Property.TYPE_CHOICES, "genders": Property.GENDER_CHOICES},
    )


def property_detail(request, pk):
    prop = get_object_or_404(Property.objects.select_related("owner"), pk=pk)
    is_favourite = (
        request.user.is_authenticated
        and Favourite.objects.filter(user=request.user, property=prop).exists()
    )
    return render(
        request,
        "properties/detail.html",
        {
            "property": prop,
            "reviews": prop.reviews.select_related("user").order_by("-created_at"),
            "is_favourite": is_favourite,
            "review_form": ReviewForm(),
            "report_form": ReportForm(),
        },
    )


@login_required
def property_create(request):
    if not request.user.is_owner:
        messages.error(request, "You do not have permission to add properties.")
        raise PermissionDenied
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.owner = request.user
            prop.is_verified = False
            prop.save()
            messages.success(request, "Property submitted successfully and is waiting for verification.")
            return redirect("properties:detail", pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, "properties/form.html", {"form": form, "title": "Add property"})


@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner != request.user and not request.user.is_platform_admin:
        messages.error(request, "You do not have permission to edit this property.")
        raise PermissionDenied
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated.")
            return redirect("properties:detail", pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    return render(request, "properties/form.html", {"form": form, "title": "Edit property"})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if prop.owner != request.user and not request.user.is_platform_admin:
        raise PermissionDenied
    prop.delete()
    messages.success(request, "Property deleted.")
    return redirect("accounts:dashboard")


@login_required
def my_properties(request):
    listings = Property.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "properties/my_properties.html", {"listings": listings})


@login_required
def property_verify(request, pk, action):
    if not request.user.is_platform_admin:
        raise PermissionDenied
    prop = get_object_or_404(Property, pk=pk)
    prop.is_verified = action == "verify"
    prop.save(update_fields=["is_verified"])
    messages.success(request, f"Listing {'verified' if prop.is_verified else 'marked pending'}.")
    return redirect("accounts:dashboard")


def about(request):
    return render(request, "properties/about.html")


def contact(request):
    if request.method == "POST":
        messages.success(request, "Thanks for reaching out. We'll reply within 24 hours.")
        return redirect("properties:contact")
    return render(request, "properties/contact.html")


def privacy(request):
    return render(request, "properties/privacy.html")


def terms(request):
    return render(request, "properties/terms.html")


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)
