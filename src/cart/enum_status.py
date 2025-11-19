
from enum import Enum
class OrderStatusEnum(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    PAID = "paid"

