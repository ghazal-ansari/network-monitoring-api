from flask import Flask

from app.database.db import init_db


def create_app():
    app = Flask(__name__)

    init_db()

    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "service": "network-monitoring-api"
        }

    return app