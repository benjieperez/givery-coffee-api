from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.database import DATABASE_CONFIG
from app.repositories.recipe_repository import RecipeRepository
from app.routers.recipe_router import RecipeRouter, router


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield

def create_app() -> FastAPI:
    application = FastAPI(
        title="Recipes API",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    register_tortoise(
        application,
        config=DATABASE_CONFIG,
        generate_schemas=False,
        add_exception_handlers=True,
    )

    repository = RecipeRepository()
    RecipeRouter(repository=repository)
    application.include_router(router)

    return application