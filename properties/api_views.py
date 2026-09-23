from rest_framework import generics, permissions, status
from rest_framework.response import Response

from favourites.models import Favourite
from reports.models import Report
from reviews.models import Review

from .models import Property
from .serializers import (
    FavouriteSerializer,
    PropertySerializer,
    ReportSerializer,
    ReviewSerializer,
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_platform_admin


class PropertyListCreate(generics.ListCreateAPIView):
    """GET /api/properties/  ·  POST /api/properties/"""

    serializer_class = PropertySerializer

    def get_queryset(self):
        qs = Property.objects.filter(is_active=True)
        params = self.request.query_params
        if params.get("location"):
            qs = qs.filter(location__icontains=params["location"])
        if params.get("max_rent"):
            qs = qs.filter(monthly_rent__lte=params["max_rent"])
        if params.get("property_type"):
            qs = qs.filter(property_type=params["property_type"])
        return qs

    def perform_create(self, serializer):
        if not self.request.user.is_owner:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Only property owners can create listings.")
        serializer.save(owner=self.request.user, is_verified=False)


class PropertyDetail(generics.RetrieveUpdateDestroyAPIView):
    """GET / PUT / DELETE /api/properties/<id>/"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class ReviewCreate(generics.CreateAPIView):
    """POST /api/reviews/"""

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review, created = Review.objects.update_or_create(
            property=serializer.validated_data["property"],
            user=request.user,
            defaults={
                "rating": serializer.validated_data["rating"],
                "comment": serializer.validated_data.get("comment", ""),
            },
        )
        out = self.get_serializer(review).data
        return Response(out, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ReportCreate(generics.CreateAPIView):
    """POST /api/reports/"""

    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=Report.PENDING)


class FavouriteCreate(generics.CreateAPIView):
    """POST /api/favourites/"""

    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fav, created = Favourite.objects.get_or_create(
            property=serializer.validated_data["property"], user=request.user
        )
        return Response(
            self.get_serializer(fav).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
