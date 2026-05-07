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
async def test_delete_recipe_success():

    await init_db()

    # Create recipe to delete
    recipe = await Recipe.create(
        title="Tomato Soup",
        making_time="15 min",
        serves="5 people",
        ingredients="onion, tomato, seasoning, water",
        cost="450"
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.delete(f"/recipes/{recipe.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Recipe successfully removed!"

    # Verify recipe is deleted
    deleted_recipe = await Recipe.filter(id=recipe.id).first()

    assert deleted_recipe is None

    await close_db()


@pytest.mark.asyncio
async def test_delete_recipe_not_found():

    await init_db()

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.delete("/recipes/9999")

    assert response.status_code == 404

    data = response.json()

    assert data["message"] == "No recipe found"

    await close_db()