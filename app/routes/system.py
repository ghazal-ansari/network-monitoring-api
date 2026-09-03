from flask import Blueprint

from app.services.system_service import get_system_metrics
from app.utils.security import jwt_required


system_bp = Blueprint("system", __name__)


@system_bp.get("/api/system")
@jwt_required
def system_metrics():
    return get_system_metrics()