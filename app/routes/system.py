from flask import Blueprint

from app.services.system_service import get_system_metrics


system_bp = Blueprint("system", __name__)


@system_bp.get("/api/system")
def system_metrics():
    return get_system_metrics()