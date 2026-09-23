from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("add/<int:property_id>/", views.add_report, name="add"),
    path("mine/", views.my_reports, name="mine"),
    path("<int:pk>/status/<str:status>/", views.update_status, name="status"),
]
