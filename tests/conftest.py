import os
import sys
from pathlib import Path
import tempfile
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.database.db import init_db
from app.utils.security import create_access_token


@pytest.fixture
def app(tmp_path):
    test_db_path = str(tmp_path / "test_monitoring.db")
    os.environ["DATABASE_PATH"] = test_db_path
    os.environ["SECRET_KEY"] = "test-secret-key-minimum-32-bytes-for-jwt-hs256"

    app = create_app()
    app.config.update({
        "TESTING": True,
        "DATABASE_PATH": test_db_path
    })

    with app.app_context():
        init_db()

    yield app

    if os.path.exists(test_db_path):
        try:
            os.remove(test_db_path)
        except OSError:
            pass


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    token = create_access_token(user_id=1, username="testadmin", role="user")
    return {
        "Authorization": f"Bearer {token}"
    }
