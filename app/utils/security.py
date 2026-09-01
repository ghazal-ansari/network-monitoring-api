import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "change-this-secret-key"


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


def create_access_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
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