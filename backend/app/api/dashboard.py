from fastapi import APIRouter

from app.models.dashboard import Dashboard
from app.services.dashboard_service import build_dashboard


router = APIRouter()


@router.get("/dashboard", response_model=Dashboard)
def get_dashboard() -> Dashboard:
    return build_dashboard()
