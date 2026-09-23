from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property

from .models import Favourite


@login_required
def toggle_favourite(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)
    fav, created = Favourite.objects.get_or_create(user=request.user, property=prop)
    if not created:
        fav.delete()
        messages.info(request, "Removed from favourites.")
    else:
        messages.success(request, "Saved to your favourites.")
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("properties:detail", pk=prop.pk)


@login_required
def my_favourites(request):
    favourites = Favourite.objects.filter(user=request.user).select_related("property")
    return render(request, "favourites/my_favourites.html", {"favourites": favourites})
