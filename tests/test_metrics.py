def test_collect_metrics_unauthorized(client):
    response = client.post("/api/metrics/collect")
    assert response.status_code == 401


def test_collect_metrics_authorized(client, auth_headers):
    response = client.post("/api/metrics/collect", headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()

    assert data["message"] == "Metrics collected successfully"
    assert "metrics" in data
    metrics = data["metrics"]
    assert "cpu_usage" in metrics
    assert "memory_usage" in metrics
    assert "disk_usage" in metrics
    assert "bytes_sent" in metrics
    assert "bytes_received" in metrics


def test_latest_metrics_empty(client, auth_headers):
    response = client.get("/api/metrics/latest", headers=auth_headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "No metrics available"


def test_latest_and_history_after_collection(client, auth_headers):
    # Collect two metric samples
    client.post("/api/metrics/collect", headers=auth_headers)
    client.post("/api/metrics/collect", headers=auth_headers)

    # Test latest
    latest_res = client.get("/api/metrics/latest", headers=auth_headers)
    assert latest_res.status_code == 200
    latest_data = latest_res.get_json()
    assert "id" in latest_data
    assert "cpu_usage" in latest_data
    assert "created_at" in latest_data

    # Test history
    history_res = client.get("/api/metrics/history", headers=auth_headers)
    assert history_res.status_code == 200
    history_data = history_res.get_json()
    assert history_data["count"] == 2
    assert len(history_data["metrics"]) == 2

    # Test history with limit
    limited_res = client.get("/api/metrics/history?limit=1", headers=auth_headers)
    assert limited_res.status_code == 200
    limited_data = limited_res.get_json()
    assert limited_data["count"] == 1
    assert len(limited_data["metrics"]) == 1


def test_history_limit_validation(client, auth_headers):
    # Limit < 1
    res1 = client.get("/api/metrics/history?limit=0", headers=auth_headers)
    assert res1.status_code == 400

    # Limit > 100
    res2 = client.get("/api/metrics/history?limit=101", headers=auth_headers)
    assert res2.status_code == 400

    # Non-integer limit
    res3 = client.get("/api/metrics/history?limit=abc", headers=auth_headers)
    assert res3.status_code == 400
