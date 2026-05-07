from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import init_db, close_db
from app.repositories.recipe_repository import RecipeRepository
from app.routers.recipe_router import RecipeRouter, router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Tortoise ORM startup / shutdown using FastAPI's lifespan protocol."""
    await init_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    application = FastAPI(
        title="Recipes API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Wire repository → router
    repository = RecipeRepository()
    RecipeRouter(repository=repository)

    application.include_router(router)
    return application