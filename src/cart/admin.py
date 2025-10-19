from django.contrib import admin

from unfold.admin import ModelAdmin

from src.cart.models import CartModel


# Register your models here.

@admin.register(CartModel)
class CartAdmin(ModelAdmin):
    list_display = ("id", "product", "quantity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("product__name",)
    list_per_page = 20
