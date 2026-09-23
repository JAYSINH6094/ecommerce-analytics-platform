from fastapi import FastAPI

from api.routes.orders import router as orders_router
from api.routes.analytics import router as analytics_router


app = FastAPI(
    title="E-Commerce Real-Time Analytics API",
    description=(
        "REST API for real-time e-commerce "
        "order ingestion and analytics."
    ),
    version="1.0.0"
)


app.include_router(orders_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": (
            "E-Commerce Real-Time Analytics API"
        ),
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }