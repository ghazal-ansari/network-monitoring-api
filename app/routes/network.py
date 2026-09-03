from flask import Blueprint

from app.services.network_service import get_network_metrics
from app.utils.security import jwt_required


network_bp = Blueprint("network", __name__)


@network_bp.get("/api/network")
@jwt_required
def network_metrics():
    return get_network_metrics()