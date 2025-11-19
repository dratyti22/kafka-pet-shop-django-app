import json
import uuid

from django.contrib.auth import get_user_model
from django.db import transaction

from src.cart.models import CartModel, OrderModel, OrderItemModel
from src.services.kafka_producer import get_kafka_producer

User = get_user_model()


class OrderService:
    @staticmethod
    def checkout(user: User, cart: list):
        with transaction.atomic():
            order = OrderModel.objects.create(user=user)
            cart_items = CartModel.objects.filter(id__in=cart, user=user)
            total_amount = 0
            for item in cart_items:
                OrderItemModel.objects.create(order=order, product=item.product, quantity=item.quantity,
                                              price=item.product.final_price)
                total_amount += item.product.final_price * item.quantity
                item.delete()

            order.total_amount = total_amount
            order.save()

            cart_event = {
                "event_id": str(uuid.uuid4()),
                "event_type": "cart.created",
                "event_version": "1.0",
                "created_at": order.created_at.isoformat(),
                "event_data": {
                    "user_id": str(user.id),
                    "user_email": user.email,
                    "user_first_name": user.first_name,
                    "user_last_name": user.last_name,
                    "total_amount": total_amount,
                    "cart_items": [
                        {
                            "product_id":str( item.product.id),
                            "product_name": item.product.name,
                            "price": str(item.product.final_price),
                            "quantity": item.quantity
                        } for item in cart_items
                    ]
                }
            }
            producer = get_kafka_producer()
            cart_event_bytes = json.dumps(cart_event).encode("utf-8")
            producer.produce(topic="order", value=cart_event_bytes, key=str(user.id).encode("utf-8"))
            producer.flush()
            return order
