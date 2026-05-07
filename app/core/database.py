import os
from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()

TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": {
            "engine":      "tortoise.backends.mysql",
            "credentials": {
                "host":     None,
                "port":     None,
                "user":     None,
                "password": None,
                "database": None,
                "ssl":      True,
            },
        }
    },
    "apps": {
        "models": {
            "models":           ["app.models.recipe"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
}


def _parse_uri(uri: str) -> dict:
    """
    Parse  mysql://user:password@host:port/dbname?ssl-mode=REQUIRED
    into a credentials dict for Tortoise's MySQL backend.
    """
    import re
    m = re.match(
        r"mysql://(?P<user>[^:]+):(?P<password>[^@]+)"
        r"@(?P<host>[^:]+):(?P<port>\d+)/(?P<database>[^?]+)",
        uri,
    )
    if not m:
        raise ValueError(f"Cannot parse DB_URI: {uri!r}")
    return {
        "host":     m.group("host"),
        "port":     int(m.group("port")),
        "user":     m.group("user"),
        "password": m.group("password"),
        "database": m.group("database"),
        "ssl":      "ssl-mode=REQUIRED" in uri,
    }


async def init_db() -> None:
    uri = os.getenv("DB_URI")
    if not uri:
        raise RuntimeError("DB_URI is not set in your .env file")

    creds = _parse_uri(uri)
    TORTOISE_ORM_CONFIG["connections"]["default"]["credentials"] = creds

    await Tortoise.init(config=TORTOISE_ORM_CONFIG)
    await Tortoise.generate_schemas(safe=True)


async def close_db() -> None:
    await Tortoise.close_connections()