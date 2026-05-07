import pytest

from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from main import app
from app.models.recipe import Recipe


async def init_db():
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.recipe"]}
    )

    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_patch_recipe():

    await init_db()

    # Create initial recipe
    recipe = await Recipe.create(
        title="Old Soup",
        making_time="10 min",
        serves="2 people",
        ingredients="water, salt",
        cost="200"
    )

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
    ) as client:

        response = await client.patch(
            f"/recipes/{recipe.id}",
            json=payload
        )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Recipe successfully updated!"

    assert "recipe" in data
    assert isinstance(data["recipe"], list)

    updated_recipe = data["recipe"][0]

    assert updated_recipe["title"] == "Tomato Soup"
    assert updated_recipe["making_time"] == "15 min"
    assert updated_recipe["serves"] == "5 people"
    assert updated_recipe["ingredients"] == "onion, tomato, seasoning, water"
    assert updated_recipe["cost"] == 450

    await close_db()