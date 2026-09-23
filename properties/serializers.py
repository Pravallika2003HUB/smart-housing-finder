from rest_framework import serializers

from favourites.models import Favourite
from reports.models import Report
from reviews.models import Review

from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ["owner", "is_verified", "created_at", "updated_at"]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "property", "user", "user_name", "rating", "comment", "created_at"]
        read_only_fields = ["user", "created_at"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "property", "user", "reason", "description", "status", "created_at"]
        read_only_fields = ["user", "status", "created_at"]


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ["id", "property", "user", "created_at"]
        read_only_fields = ["user", "created_at"]
