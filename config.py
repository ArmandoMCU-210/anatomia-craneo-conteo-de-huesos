import os

from sqlalchemy.pool import NullPool

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Vercel define automáticamente la variable de entorno VERCEL=1 en producción.
IS_VERCEL = bool(os.environ.get("VERCEL"))


def _normalize_db_url(url):
    # Algunos proveedores (Heroku, Vercel Postgres) entregan URLs con el esquema
    # "postgres://", pero SQLAlchemy 1.4+ / psycopg2 requieren "postgresql://".
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


def _default_sqlite_uri():
    if IS_VERCEL:
        # El sistema de archivos del proyecto es de solo lectura en Vercel; solo /tmp
        # admite escritura y no persiste entre invocaciones. Sin DATABASE_URL apuntando
        # a una base de datos real, el historial de intentos se reiniciará seguido.
        return "sqlite:////tmp/attempts.db"
    return f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'attempts.db')}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-cambiar-en-produccion")

    _env_url = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(_env_url) if _env_url else _default_sqlite_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # En serverless conviene no mantener un pool de conexiones entre invocaciones.
    SQLALCHEMY_ENGINE_OPTIONS = {"poolclass": NullPool} if IS_VERCEL else {}
