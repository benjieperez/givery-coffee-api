# conftest.py

import asyncio
import pytest
from httpx import AsyncClient
from tortoise import Tortoise

from main import app  # change to your FastAPI/Starlette app import


TEST_DB_URL = "sqlite://:memory:"


# -----------------------------------
# Event Loop
# -----------------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# -----------------------------------
# Initialize Tortoise ORM
# -----------------------------------
@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={
            "models": ["models"]  # change to your models module
        },
    )

    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()


# -----------------------------------
# HTTP Client
# -----------------------------------
@pytest.fixture
async def client():
    async with AsyncClient(
        app=app,
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def clean_db():
    yield

    conn = Tortoise.get_connection("default")

    for table in reversed(Tortoise.apps.get("models", {}).values()):
        await conn.execute_query(
            f'DELETE FROM "{table._meta.db_table}";'
        )