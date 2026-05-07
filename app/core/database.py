from decouple import config as env
from urllib.parse import quote_plus


def _get_tortoise_engine(db_engine: str) -> str:
    engines = {
        "postgres": "tortoise.backends.asyncpg",
        "mysql": "tortoise.backends.mysql",
        "mariadb": "tortoise.backends.mysql",
        "sqlite": "tortoise.backends.sqlite",
    }
    engine = engines.get(db_engine.lower())
    if not engine:
        raise ValueError(f"Unsupported DB_ENGINE: '{db_engine}'. Choose from: {list(engines.keys())}")
    return engine

def _build_config() -> dict:
    db_engine = env("DB_ENGINE")
    db_user = env("DB_USER")
    db_password = quote_plus(env("DB_PASSWORD"))
    db_name = env("DB_NAME")
    db_host = env("DB_HOST", default="localhost")
    db_port = env("DB_PORT", cast=int)

    tortoise_engine = _get_tortoise_engine(db_engine)

    credentials = {
        "database": db_name,
        "host": db_host,
        "port": db_port,
        "user": db_user,
        "password": db_password,
    }

    if db_engine.lower() == "sqlite":
        credentials = {"file_path": db_name}

    return {
        "connections": {
            "default": {
                "engine": tortoise_engine,
                "credentials": credentials,
            }
        },
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "default",
            }
        },
    }

DATABASE_CONFIG = _build_config()