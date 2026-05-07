from typing import Optional

from app.models.recipe import Recipe


class RecipeRepository:
    async def get_all(self) -> list[Recipe]:
        return await Recipe.all()

    async def get_by_id(self, recipe_id: int) -> Optional[Recipe]:
        return await Recipe.get_or_none(id=recipe_id)

    async def create(
        self,
        title: str,
        making_time: str,
        serves: str,
        ingredients: str,
        cost: int,
    ) -> Recipe:
        return await Recipe.create(
            title=title,
            making_time=making_time,
            serves=serves,
            ingredients=ingredients,
            cost=cost,
        )

    async def update(self, recipe_id: int, fields: dict) -> Optional[Recipe]:
        recipe = await self.get_by_id(recipe_id)
        if recipe is None:
            return None
        await recipe.update_from_dict(fields).save()
        return recipe

    async def delete(self, recipe_id: int) -> bool:
        recipe = await self.get_by_id(recipe_id)
        if recipe is None:
            return False
        await recipe.delete()
        return True