import pytest

from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from main import app

async def init_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.recipe"]}
    )

    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_create_recipe_success():

    await init_db()

    payload = {
        "title": "Tomato Soup",
        "making_time": "15 min",
        "serves": "5 people",
        "ingredients": "onion, tomato, seasoning, water",
        "cost": "450"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post(
            "/recipes",
            json=payload
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Recipe successfully created!"

    recipe = data["recipe"][0]

    assert recipe["title"] == payload["title"]

    await close_db()


@pytest.mark.asyncio
async def test_create_recipe_validation_error():

    await init_db()

    payload = {
        "title": "Tomato Soup"
    }

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post(
            "/recipes",
            json=payload
        )

    
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Recipe creation failed!"

    missing_fields = data["required"].split(", ")

    assert "making_time" in missing_fields
    assert "serves" in missing_fields
    assert "ingredients" in missing_fields
    assert "cost" in missing_fields

    await close_db()