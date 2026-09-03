from datetime import datetime, timedelta, timezone
from functools import wraps
import os
import bcrypt
import jwt
from flask import request, g, jsonify


SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def create_access_token(user_id, username, role="user"):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def decode_token(token):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"error": "Authorization header is missing"}, 401

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {"error": "Invalid authorization header format. Expected 'Bearer <token>'"}, 401

        token = parts[1]

        try:
            payload = decode_token(token)
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid or corrupted token"}, 401

        return f(*args, **kwargs)

    return decorated
