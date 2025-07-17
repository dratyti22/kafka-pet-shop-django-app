def photo_product_path(instance, filename):
    return f"media/photo/products/{instance.product.id}/{filename}"
