from django.urls import path

from . import api_views

urlpatterns = [
    path("properties/", api_views.PropertyListCreate.as_view(), name="api-properties"),
    path("properties/<int:pk>/", api_views.PropertyDetail.as_view(), name="api-property-detail"),
    path("reviews/", api_views.ReviewCreate.as_view(), name="api-review-create"),
    path("reports/", api_views.ReportCreate.as_view(), name="api-report-create"),
    path("favourites/", api_views.FavouriteCreate.as_view(), name="api-favourite-create"),
]
