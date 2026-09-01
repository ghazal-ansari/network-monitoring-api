
from flask import Blueprint

from app.services.network_service import get_network_metrics


network_bp = Blueprint("network", __name__)


@network_bp.get("/api/network")
def network_metrics():
    return get_network_metrics()