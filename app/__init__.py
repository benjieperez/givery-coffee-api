from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from app.core.database import DATABASE_CONFIG
from app.repositories.recipe_repository import RecipeRepository
from app.routers.recipe_router import RecipeRouter, router


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    missing_fields = [err["loc"][-1] for err in exc.errors() if err["type"] == "missing"]
    return JSONResponse(
        status_code=200,
        content={
            "message": "Recipe creation failed!",
            "required": ", ".join(missing_fields) if missing_fields else "title, making_time, serves, ingredients, cost",
        }
    )


def create_app() -> FastAPI:
    application = FastAPI(
        title="Recipes API",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    application.add_exception_handler(RequestValidationError, validation_exception_handler)

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