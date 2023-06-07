from fastapi import APIRouter

from app.api.api_v1.endpoints import records

api_router = APIRouter()
api_router.include_router(records.router, prefix="/records", tags=["records"])