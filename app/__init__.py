from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import Database
from tortoise import Tortoise
from app.repositories.recipe_repository import RecipeRepository
from app.routers.recipe_router import RecipeRouter, router

db = Database()

@asynccontextmanager
async def lifespan(application: FastAPI):
    await db.init_db()
    yield
    await Tortoise.close_connections()


def create_app() -> FastAPI:
    application = FastAPI(
        title="Recipes API",
        version="1.0.0",
        lifespan=lifespan,
    )
    repository = RecipeRepository()
    RecipeRouter(repository=repository)

    application.include_router(router)
    return application