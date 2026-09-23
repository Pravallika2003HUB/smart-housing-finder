from django.urls import path

from . import views

app_name = "properties"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.property_search, name="search"),
    path("property/<int:pk>/", views.property_detail, name="detail"),
    path("property/add/", views.property_create, name="create"),
    path("property/<int:pk>/edit/", views.property_edit, name="edit"),
    path("property/<int:pk>/delete/", views.property_delete, name="delete"),
    path("property/<int:pk>/<str:action>/moderate/", views.property_verify, name="moderate"),
    path("my-properties/", views.my_properties, name="mine"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
