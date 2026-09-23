from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    TIMESTAMP,
    text
)

from api.database import Base


class RealtimeOrder(Base):
    __tablename__ = "realtime_orders"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    product_category = Column(
        String(100),
        nullable=False,
        index=True
    )

    price = Column(
        Numeric(12, 2),
        nullable=False
    )

    freight_value = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    customer_state = Column(
        String(10),
        nullable=False,
        index=True
    )

    payment_type = Column(
        String(30),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    order_timestamp = Column(
        DateTime,
        nullable=False,
        index=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text(
            "CURRENT_TIMESTAMP"
        )
    )