from rest_framework import serializers

from src.product.models import CategoryModel, ProductModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("name", "slug", "parent")


class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ("name", "slug", "description_short", "price", "discount", "is_popular", "is_new","is_active")
        read_only_fields = ("is_active","slug")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ("id", "name", "slug", "description",
                  "description_short", "category", "user", "quantity", "sales_count", "price",
                  "discount", "created_at", "updated_at", "is_active", "is_popular", "is_new")
        read_only_fields = ("id", "created_at", "updated_at", "user", "slug","sales_count")
