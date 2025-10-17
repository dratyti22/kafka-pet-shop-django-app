import logging

from confluent_kafka import Producer

from django.conf import settings

logger = logging.getLogger(__name__)
logger.level = logging.INFO


def get_kafka_producer() -> Producer:
    try:
        config = {
            'bootstrap.servers': settings.KAFKA_URL,
            'retries': 3,
            'linger.ms': 10,
            'request.timeout.ms': 30000,
            'delivery.timeout.ms': 60000,
            'socket.timeout.ms': 10000,
        }
        logger.info(f"Initializing Kafka producer with config: {config}")
        producer = Producer(config)
        logger.info("KafkaProducer initialized successfully")
        return producer
    except Exception as ex:
        logger.error(f"The initialization error KafkaProducer: {ex}")
        raise
