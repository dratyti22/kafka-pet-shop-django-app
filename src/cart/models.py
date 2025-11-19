from django.db import models

from src.cart.enum_status import OrderStatusEnum


class CartModel(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('product.ProductModel', on_delete=models.CASCADE, related_name='cart')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ('-created_at',)
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        app_label = 'cart'

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.quantity}"


class OrderModel(models.Model):


    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.Choices(OrderStatusEnum, default='pending', max_length=20)
    url = models.URLField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        app_label = 'cart'

    def __str__(self):
        return f"{self.user.email} - {self.status}"


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.ProductModel', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        app_label = 'cart'

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"
