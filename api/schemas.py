from datetime import datetime

from pydantic import BaseModel, Field


class RealtimeOrderCreate(BaseModel):
    order_id: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    customer_id: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    product_category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    price: float = Field(
        ...,
        gt=0
    )

    freight_value: float = Field(
        default=0.0,
        ge=0
    )

    customer_state: str = Field(
        ...,
        min_length=2,
        max_length=10
    )

    payment_type: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

    quantity: int = Field(
        default=1,
        gt=0
    )

    order_timestamp: datetime