from django.contrib import admin
from unfold.admin import ModelAdmin

from src.product.models import CategoryModel, PhotoProductModel, ProductModel


@admin.register(CategoryModel)
class CategoryAdmin(ModelAdmin):
    pass


class PhotoProductInline(admin.TabularInline):
    fk_name = "product"
    model = PhotoProductModel


@admin.register(ProductModel)
class ProductAdmin(ModelAdmin):
    inlines = [PhotoProductInline, ]
