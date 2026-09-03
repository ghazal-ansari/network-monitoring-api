from flask import Flask, jsonify

from app.database.db import init_db
from app.routes.auth import auth_bp
from app.routes.metrics import metrics_bp
from app.routes.network import network_bp
from app.routes.system import system_bp


def create_app():
    app = Flask(__name__)

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(metrics_bp)

    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "service": "network-monitoring-api"
        }

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app