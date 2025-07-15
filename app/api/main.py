from fastapi import FastAPI
from app.api.v1.routers import car_router

app = FastAPI(title="RAGCar CS2")

app.include_router(car_router.router, prefix="/api/v1")
