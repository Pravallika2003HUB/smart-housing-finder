from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("properties.urls")),
    path("accounts/", include("accounts.urls")),
    path("reviews/", include("reviews.urls")),
    path("reports/", include("reports.urls")),
    path("favourites/", include("favourites.urls")),
    path("api/", include("properties.api_urls")),
]

handler404 = "properties.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
