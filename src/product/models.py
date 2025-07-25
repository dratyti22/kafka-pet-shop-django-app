import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Max
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from src.services.image import photo_product_path

User = get_user_model()


class CategoryModel(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"
        app_label = "product"

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    description_short = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(to=CategoryModel, on_delete=models.CASCADE, related_name="products")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveIntegerField()
    sales_count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                   validators=[MaxValueValidator(100), MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        app_label = "product"
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["slug"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="unique_product_name_category"
            )
        ]

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.is_active = self.quantity > 0
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while ProductModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class PhotoProductModel(models.Model):
    product = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE, related_name="photos",
                                db_index=True)

    image = models.ImageField(upload_to=photo_product_path)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photos"
        app_label = "product"
        ordering = ['order']

    def __str__(self):
        return f"{self.image} - {self.order}"

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = PhotoProductModel.objects.filter(product=self.product).aggregate(Max("order"))[
                "order__max"]
            self.order = max_order + 1 if max_order else 1
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    key = models.CharField(max_length=120)
    value = models.TextField()

    class Meta:
        verbose_name = "attribute"
        verbose_name_plural = "attributes"
        app_label = "product"

    def __str__(self):
        return f"{self.key:30} - {self.value:30}"
