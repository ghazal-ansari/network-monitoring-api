from flask import Flask

from app.database.db import init_db
from app.routes.metrics import metrics_bp
from app.routes.network import network_bp
from app.routes.system import system_bp


def create_app():
    app = Flask(__name__)

    init_db()

    app.register_blueprint(system_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(metrics_bp)

    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "service": "network-monitoring-api"
        }

    return app