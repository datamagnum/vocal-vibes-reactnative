import logging

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from app.core.config import settings
from app.exceptions.exceptions_http import HTTPERROR, http_error_handler
from app.routes.api import api_v1_router


def create_app() -> FastAPI:
    logging.getLogger("uvicorn.access")
    logger.info("Initiliase fast-API app")

    app = FastAPI(
        title=settings.PROJECT_NAME,
    )
    app.openapi_version = "3.0.3"

    app.include_router(api_v1_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS Middleware initialized {settings.allowed_origins_list=}")

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    app.add_exception_handler(HTTPERROR, http_error_handler)

    use_route_names_as_operation_ids(app)

    return app


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            if "Internal" in route.tags:
                route.operation_id = f"internal_{route.name}"
            else:
                route.operation_id = route.name


try:
    app = create_app()
except Exception as e:
    logger.error(f"Error in fast-API app initialisation => {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000, log_level="info")
