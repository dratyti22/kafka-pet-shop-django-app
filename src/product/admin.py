from django.contrib import admin
from unfold.admin import ModelAdmin

from src.product.models import AttributeProductModel, CategoryModel, PhotoProductModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class PhotoProductInline(admin.TabularInline):
    fk_name = "product"
    model = PhotoProductModel


class AttributeProductInline(admin.TabularInline):
    fk_name = "product"
    model = AttributeProductModel


@admin.register(AttributeProductModel)
class AttributeProductAdmin(ModelAdmin):
    list_display = ["product","short_key"]

    def short_key(self, obj):
        return obj.key[:30]


@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    list_display = ["name", "price", "is_active"]
    inlines = [PhotoProductInline, AttributeProductInline]
    prepopulated_fields = {"slug": ("name",)}
