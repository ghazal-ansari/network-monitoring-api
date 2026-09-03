def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "username": "alice",
        "password": "secretpassword"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "alice"
    assert "password_hash" not in data["user"]


def test_register_duplicate_username(client):
    client.post("/api/auth/register", json={
        "username": "bob",
        "password": "secretpassword"
    })
    response = client.post("/api/auth/register", json={
        "username": "bob",
        "password": "secretpassword2"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert "already exists" in data["error"]


def test_register_validation_errors(client):
    # Missing username
    res1 = client.post("/api/auth/register", json={"password": "secretpassword"})
    assert res1.status_code == 400

    # Short password
    res2 = client.post("/api/auth/register", json={"username": "carol", "password": "123"})
    assert res2.status_code == 400

    # Empty payload
    res3 = client.post("/api/auth/register")
    assert res3.status_code == 400


def test_login_success(client):
    client.post("/api/auth/register", json={
        "username": "david",
        "password": "password123"
    })
    response = client.post("/api/auth/login", json={
        "username": "david",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["username"] == "david"


def test_login_invalid_credentials(client):
    client.post("/api/auth/register", json={
        "username": "eve",
        "password": "password123"
    })

    # Wrong password
    res1 = client.post("/api/auth/login", json={
        "username": "eve",
        "password": "wrongpassword"
    })
    assert res1.status_code == 401

    # Non-existent user
    res2 = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "password123"
    })
    assert res2.status_code == 401


def test_me_endpoint(client):
    # Register & Login
    client.post("/api/auth/register", json={
        "username": "frank",
        "password": "password123"
    })
    login_res = client.post("/api/auth/login", json={
        "username": "frank",
        "password": "password123"
    })
    token = login_res.get_json()["access_token"]

    # Valid token
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["username"] == "frank"
    assert data["role"] == "user"

    # Missing auth header
    res_no_auth = client.get("/api/auth/me")
    assert res_no_auth.status_code == 401

    # Invalid token format
    res_bad_format = client.get("/api/auth/me", headers={"Authorization": "Token 12345"})
    assert res_bad_format.status_code == 401

    # Invalid token content
    res_bad_token = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    assert res_bad_token.status_code == 401
