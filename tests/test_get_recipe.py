import pytest
from httpx import AsyncClient, ASGITransport
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
async def test_get_recipes():

    await init_db()

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        # First create a recipe (so GET has data)
        await ac.post("/recipes", json={
            "title": "Chicken Curry",
            "making_time": "45 min",
            "serves": "4 people",
            "ingredients": "onion, chicken, seasoning",
            "cost": 1000
        })

        response = await ac.get("/recipes")

    assert response.status_code == 200

    data = response.json()

    assert "recipes" in data
    assert isinstance(data["recipes"], list)

    assert len(data["recipes"]) >= 1

    recipe = data["recipes"][0]

    assert "id" in recipe
    assert "title" in recipe
    assert "making_time" in recipe
    assert "serves" in recipe
    assert "ingredients" in recipe
    assert "cost" in recipe