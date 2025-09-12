from rest_framework import serializers

from src.product.models import CategoryModel, ProductModel, PhotoProductModel, AttributeProductModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("name", "slug", "parent")


class PhotoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoProductModel
        fields = ("product", "image", "is_main", "order")


class AttributeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeProductModel
        fields = ("product", "key", "value")


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ("name", "description", "description_short", "category", "quantity", "price", "discount",
                  "slug")
        read_only_fields = ("slug",)


class ProductListSerializer(serializers.ModelSerializer):
    is_popular = serializers.SerializerMethodField(read_only=True)
    is_new = serializers.SerializerMethodField(read_only=True)
    main_photo = serializers.CharField(read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def get_is_popular(self, obj):
        return obj.is_popular

    def get_is_new(self, obj):
        return obj.is_new

    def get_final_price(self, obj):
        return obj.final_price

    class Meta:
        model = ProductModel
        fields = ("id", "name", "slug", "description_short", "price", "discount", "is_active",
                  "is_popular", "is_new", "main_photo", "final_price")


class ProductDetailSerializer(ProductListSerializer):
    photos = PhotoProductSerializer(many=True, read_only=True)
    attributes = AttributeProductSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta(ProductListSerializer.Meta):
        model = ProductModel
        fields = ("id", "name", "slug", "description", "description_short", "category",
                  "quantity", "price", "discount", "final_price", "created_at", "is_active", "is_popular",
                  "is_new", "photos", "attributes")
