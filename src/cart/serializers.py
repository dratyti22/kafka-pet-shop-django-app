from rest_framework import serializers

from src.cart.models import CartModel
from src.product.models import ProductModel


class CartProductSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    main_photo = serializers.SerializerMethodField()

    def get_main_photo(self, obj):
        return getattr(obj, 'main_photo', None)

    class Meta:
        model = ProductModel
        fields = ("id", "name", "final_price", "is_active", "main_photo")


class CartSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)

    class Meta:
        model = CartModel
        fields = ("id", "product", "quantity", "created_at")
