from fastapi import APIRouter

from app.api.endpoints import assessment

api_router = APIRouter()

api_router.include_router(assessment.router, tags=["assessment"]) 