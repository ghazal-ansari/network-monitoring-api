import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = BASE_DIR / "instance"
DEFAULT_DATABASE_PATH = DATABASE_DIR / "monitoring.db"


def get_database_path():
    env_path = os.environ.get("DATABASE_PATH")
    if env_path:
        path = Path(env_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    DATABASE_DIR.mkdir(exist_ok=True)
    return DEFAULT_DATABASE_PATH


def get_db():
    db_path = get_database_path()
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection


def init_db():
    connection = get_db()

    schema_path = Path(__file__).resolve().parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    connection.commit()
    connection.close()