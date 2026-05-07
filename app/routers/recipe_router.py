from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.repositories.recipe_repository import RecipeRepository
from app.schemas.recipe import RecipeCreateSchema, RecipeUpdateSchema

router = APIRouter(prefix="/recipes", tags=["recipes"])


class RecipeRouter:
    """
    Binds all /recipes route handlers to a FastAPI APIRouter.
    Delegates all data operations to RecipeRepository.
    """

    def __init__(self, repository: RecipeRepository) -> None:
        self._repo = repository
        self._register_routes()

    def _register_routes(self) -> None:
        router.add_api_route("",      self.create,  methods=["POST"])
        router.add_api_route("",      self.get_all, methods=["GET"])
        router.add_api_route("/{id}", self.get_one, methods=["GET"])
        router.add_api_route("/{id}", self.update,  methods=["PATCH"])
        router.add_api_route("/{id}", self.delete,  methods=["DELETE"])

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    async def create(self, payload: RecipeCreateSchema) -> JSONResponse:
        if not payload.is_valid():
            return JSONResponse(status_code=200, content={
                "message":  "Recipe creation failed!",
                "required": "title, making_time, serves, ingredients, cost",
            })
        recipe = await self._repo.create(
            title=payload.title,
            making_time=payload.making_time,
            serves=payload.serves,
            ingredients=payload.ingredients,
            cost=payload.cost,
        )
        return JSONResponse(status_code=200, content={
            "message": "Recipe successfully created!",
            "recipe":  [recipe.to_dict()],
        })

    async def get_all(self) -> JSONResponse:
        recipes = await self._repo.get_all()
        return JSONResponse(status_code=200, content={
            "recipes": [r.to_dict() for r in recipes],
        })

    async def get_one(self, id: int) -> JSONResponse:
        recipe = await self._repo.get_by_id(id)
        if recipe is None:
            return JSONResponse(status_code=200, content={"message": "No recipe found"})
        return JSONResponse(status_code=200, content={
            "message": "Recipe details by id",
            "recipe":  [recipe.to_dict()],
        })

    async def update(self, id: int, payload: RecipeUpdateSchema) -> JSONResponse:
        recipe = await self._repo.get_by_id(id)
        if recipe is None:
            return JSONResponse(status_code=200, content={"message": "No recipe found"})
        fields = {k: v for k, v in payload.model_dump().items() if v is not None}
        updated = await self._repo.update(id, fields)
        return JSONResponse(status_code=200, content={
            "message": "Recipe successfully updated!",
            "recipe":  [updated.to_dict()],
        })

    async def delete(self, id: int) -> JSONResponse:
        deleted = await self._repo.delete(id)
        if not deleted:
            return JSONResponse(status_code=200, content={"message": "No recipe found"})
        return JSONResponse(status_code=200, content={
            "message": "Recipe successfully removed!",
        })