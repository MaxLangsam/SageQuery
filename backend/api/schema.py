from fastapi import APIRouter
from backend.services.schema_discovery import get_schema_service

router = APIRouter()

@router.get("/", response_model=dict)
def get_schema():
    """Return database schema: tables and columns."""
    return get_schema_service() 