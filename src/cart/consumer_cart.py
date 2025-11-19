import json
import logging

from confluent_kafka import Consumer
from django.conf import settings

from src.cart.enum_status import OrderStatusEnum
from src.cart.models import OrderModel

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def consume_payments():
    consumer = Consumer({
        "bootstrap.servers": settings.KAFKA_URL,
        'group.id': 'orders-service',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(["payments"])
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            event = json.loads(msg.value().decode("utf-8"))
            if event["event_type"] == "payment.created":
                handle_payment_event_created(event)
            if event["event_type"] == "payment.succeeded":
                handle_payment_event_succeeded(event)
    finally:
        consumer.close()


def handle_payment_event_created(event):
    data = event["data"]
    try:
        order_id = data["order_id"]
        order = OrderModel.objects.get(id=order_id)
        order.status = OrderStatusEnum.PROCESSING.value
        order.url = data["url"]
        order.save()
        logger.info(f"Order {order.id} updated with payment URL")

    except OrderModel.DoesNotExist:
        logger.error(f"Order {data['order_id']} not found")


def handle_payment_event_succeeded(event):
    data = event["data"]
    try:
        order_id = data["order_id"]
        order = OrderModel.objects.get(id=order_id)
        order.status = OrderStatusEnum.PAID.value
        order.save()
        logger.info(f"Order {order.id} updated with status PAID")
        # TODO: отправлять на email об успешной оплаты товаров
    except OrderModel.DoesNotExist:
        logger.error(f"Order {data['order_id']} not found")
