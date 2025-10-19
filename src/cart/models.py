from django.db import models


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
