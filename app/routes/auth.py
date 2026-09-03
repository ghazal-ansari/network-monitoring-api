import sqlite3
from flask import Blueprint, request, g

from app.database.db import get_db
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    jwt_required
)


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/api/auth/register")
def register():
    data = request.get_json(silent=True)
    if not data:
        return {"error": "Invalid or missing JSON body"}, 400

    username = data.get("username")
    password = data.get("password")

    if not username or not isinstance(username, str) or not username.strip():
        return {"error": "Username is required"}, 400

    if not password or not isinstance(password, str) or len(password) < 6:
        return {"error": "Password is required and must be at least 6 characters"}, 400

    username = username.strip()

    db = get_db()
    existing_user = db.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if existing_user:
        db.close()
        return {"error": "Username already exists"}, 409

    password_hash = hash_password(password)

    cursor = db.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, "user")
    )
    db.commit()
    user_id = cursor.lastrowid
    db.close()

    return {
        "message": "User registered successfully",
        "user": {
            "id": user_id,
            "username": username,
            "role": "user"
        }
    }, 201


@auth_bp.post("/api/auth/login")
def login():
    data = request.get_json(silent=True)
    if not data:
        return {"error": "Invalid or missing JSON body"}, 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password are required"}, 400

    username = username.strip()

    db = get_db()
    user = db.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    db.close()

    if not user or not verify_password(password, user["password_hash"]):
        return {"error": "Invalid username or password"}, 401

    token = create_access_token(
        user_id=user["id"],
        username=user["username"],
        role=user["role"]
    )

    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }, 200


@auth_bp.get("/api/auth/me")
@jwt_required
def me():
    user_id = g.current_user.get("user_id")

    db = get_db()
    user = db.execute(
        "SELECT id, username, role, created_at FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    db.close()

    if not user:
        return {"error": "User not found"}, 404

    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "created_at": user["created_at"]
    }, 200
