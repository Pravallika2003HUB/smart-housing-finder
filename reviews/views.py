from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property

from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    if request.method != "POST":
        return redirect("properties:detail", pk=prop.pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.update_or_create(
            property=prop,
            user=request.user,
            defaults={"rating": form.cleaned_data["rating"], "comment": form.cleaned_data["comment"]},
        )
        messages.success(request, "Thanks! Your review has been saved.")
    else:
        messages.error(request, "Please choose a rating before submitting.")
    return redirect("properties:detail", pk=prop.pk)


@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related("property")
    return render(request, "reviews/my_reviews.html", {"reviews": reviews})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_platform_admin:
        raise PermissionDenied
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect("reviews:mine")
