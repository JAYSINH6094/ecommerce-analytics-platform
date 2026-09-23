from datetime import datetime, time

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import RealtimeOrder


router = APIRouter(
    prefix="/analytics",
    tags=["Real-Time Analytics"]
)


# ============================================================
# TODAY'S ANALYTICS
# ============================================================

@router.get("/today")
def today_analytics(
    db: Session = Depends(get_db)
):
    today = datetime.now().date()

    start_of_day = datetime.combine(
        today,
        time.min
    )

    end_of_day = datetime.combine(
        today,
        time.max
    )

    result = db.query(
        func.count(
            func.distinct(RealtimeOrder.order_id)
        ).label("orders"),

        func.coalesce(
            func.sum(
                RealtimeOrder.price
                * RealtimeOrder.quantity
            ),
            0
        ).label("revenue"),

        func.coalesce(
            func.sum(
                RealtimeOrder.quantity
            ),
            0
        ).label("items_sold")
    ).filter(
        RealtimeOrder.order_timestamp
        >= start_of_day,

        RealtimeOrder.order_timestamp
        <= end_of_day
    ).first()

    orders = result.orders or 0
    revenue = float(result.revenue or 0)
    items_sold = result.items_sold or 0

    average_order_value = (
        revenue / orders
        if orders > 0
        else 0
    )

    return {
        "date": str(today),
        "orders": orders,
        "revenue": round(revenue, 2),
        "items_sold": items_sold,
        "average_order_value": round(
            average_order_value,
            2
        )
    }


# ============================================================
# RECENT ORDERS
# ============================================================

@router.get("/recent")
def recent_orders(
    db: Session = Depends(get_db)
):
    orders = (
        db.query(RealtimeOrder)
        .order_by(
            RealtimeOrder.order_timestamp.desc()
        )
        .limit(10)
        .all()
    )

    return [
        {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "product_category": order.product_category,
            "price": float(order.price),
            "freight_value": float(
                order.freight_value
            ),
            "quantity": order.quantity,
            "customer_state": order.customer_state,
            "payment_type": order.payment_type,
            "order_timestamp": (
                order.order_timestamp.isoformat()
            )
        }
        for order in orders
    ]


# ============================================================
# CATEGORY ANALYTICS
# ============================================================

@router.get("/category")
def category_analytics(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            RealtimeOrder.product_category,

            func.count(
                func.distinct(
                    RealtimeOrder.order_id
                )
            ).label("orders"),

            func.sum(
                RealtimeOrder.price
                * RealtimeOrder.quantity
            ).label("revenue"),

            func.sum(
                RealtimeOrder.quantity
            ).label("items_sold")
        )
        .group_by(
            RealtimeOrder.product_category
        )
        .order_by(
            func.sum(
                RealtimeOrder.price
                * RealtimeOrder.quantity
            ).desc()
        )
        .all()
    )

    return [
        {
            "product_category": row.product_category,
            "orders": row.orders,
            "revenue": round(
                float(row.revenue or 0),
                2
            ),
            "items_sold": row.items_sold
        }
        for row in results
    ]


# ============================================================
# STATE ANALYTICS
# ============================================================

@router.get("/state")
def state_analytics(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            RealtimeOrder.customer_state,

            func.count(
                func.distinct(
                    RealtimeOrder.order_id
                )
            ).label("orders"),

            func.sum(
                RealtimeOrder.price
                * RealtimeOrder.quantity
            ).label("revenue"),

            func.sum(
                RealtimeOrder.quantity
            ).label("items_sold")
        )
        .group_by(
            RealtimeOrder.customer_state
        )
        .order_by(
            func.sum(
                RealtimeOrder.price
                * RealtimeOrder.quantity
            ).desc()
        )
        .all()
    )

    return [
        {
            "customer_state": row.customer_state,
            "orders": row.orders,
            "revenue": round(
                float(row.revenue or 0),
                2
            ),
            "items_sold": row.items_sold
        }
        for row in results
    ]