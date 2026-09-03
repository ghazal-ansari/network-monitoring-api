def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "network-monitoring-api"


def test_system_metrics_unauthorized(client):
    response = client.get("/api/system")
    assert response.status_code == 401


def test_system_metrics_authorized(client, auth_headers):
    response = client.get("/api/system", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert "cpu" in data
    assert "usage_percent" in data["cpu"]
    assert "cores" in data["cpu"]

    assert "memory" in data
    assert "total" in data["memory"]
    assert "used" in data["memory"]
    assert "usage_percent" in data["memory"]

    assert "disk" in data
    assert "total" in data["disk"]
    assert "used" in data["disk"]
    assert "free" in data["disk"]
    assert "usage_percent" in data["disk"]

    assert "system" in data
    assert "hostname" in data["system"]
    assert "operating_system" in data["system"]


def test_network_metrics_unauthorized(client):
    response = client.get("/api/network")
    assert response.status_code == 401


def test_network_metrics_authorized(client, auth_headers):
    response = client.get("/api/network", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()

    assert "hostname" in data
    assert "interfaces" in data
    assert isinstance(data["interfaces"], list)
    assert "traffic" in data
    assert "bytes_sent" in data["traffic"]
    assert "bytes_received" in data["traffic"]
