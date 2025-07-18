from rest_framework import serializers

from src.product.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("name", "slug", "parent")
