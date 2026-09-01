from flask import Blueprint, request

from app.database.db import get_db
from app.services.metrics_service import collect_metrics


metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.post("/api/metrics/collect")
def collect():
    metrics = collect_metrics()

    return {
        "message": "Metrics collected successfully",
        "metrics": metrics
    }, 201


@metrics_bp.get("/api/metrics/history")
def metrics_history():
    limit = request.args.get("limit", default=50, type=int)

    if limit < 1:
        return {
            "error": "limit must be greater than 0"
        }, 400

    if limit > 100:
        return {
            "error": "limit cannot be greater than 100"
        }, 400

    db = get_db()

    rows = db.execute(
        """
        SELECT
            id,
            cpu_usage,
            memory_usage,
            disk_usage,
            bytes_sent,
            bytes_received,
            created_at
        FROM monitoring_metrics
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    db.close()

    return {
        "count": len(rows),
        "metrics": [dict(row) for row in rows]
    }


@metrics_bp.get("/api/metrics/latest")
def latest_metrics():
    db = get_db()

    row = db.execute(
        """
        SELECT
            id,
            cpu_usage,
            memory_usage,
            disk_usage,
            bytes_sent,
            bytes_received,
            created_at
        FROM monitoring_metrics
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    db.close()

    if row is None:
        return {
            "message": "No metrics available"
        }, 404

    return dict(row)