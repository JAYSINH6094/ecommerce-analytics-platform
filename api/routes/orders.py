from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import RealtimeOrder
from api.schemas import RealtimeOrderCreate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: RealtimeOrderCreate,
    db: Session = Depends(get_db)
):
    new_order = RealtimeOrder(
        order_id=order.order_id,
        customer_id=order.customer_id,
        product_category=order.product_category,
        price=order.price,
        freight_value=order.freight_value,
        customer_state=order.customer_state,
        payment_type=order.payment_type,
        quantity=order.quantity,
        order_timestamp=order.order_timestamp
    )

    db.add(new_order)

    try:
        db.commit()
        db.refresh(new_order)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Order ID already exists."
        )

    return {
        "message": "Order created successfully",
        "order_id": new_order.order_id,
        "database_id": new_order.id
    }