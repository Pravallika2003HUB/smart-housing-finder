from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<int:property_id>/", views.add_review, name="add"),
    path("mine/", views.my_reviews, name="mine"),
    path("<int:pk>/delete/", views.delete_review, name="delete"),
]
