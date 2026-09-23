from django.urls import path

from . import views

app_name = "favourites"

urlpatterns = [
    path("toggle/<int:property_id>/", views.toggle_favourite, name="toggle"),
    path("", views.my_favourites, name="mine"),
]
