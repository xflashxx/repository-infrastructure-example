from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends, FastAPI, Request, Security
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from repository_infrastructure_example import __appname__, __version__
from repository_infrastructure_example.application.api import routers
from repository_infrastructure_example.application.api.authentication.documentation import (
    verify_documentation_access,
)
from repository_infrastructure_example.application.api.authentication.endpoints import (
    verify_endpoint_access,
)
from repository_infrastructure_example.application.api.responses import (
    ErrorResponseModel,
)
from repository_infrastructure_example.application.context import ApplicationContext
from repository_infrastructure_example.exceptions import HTTPError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set up application context
    context = ApplicationContext()

    # Log all settings when the application starts.
    context.log_settings()

    # Run database migrations
    context.clients.postgres.run_migrations()

    # Store application context
    app.state.context = context

    # Yield control to the application
    yield


# Create the FastAPI application
app = FastAPI(
    title=__appname__,
    version=__version__,
    lifespan=lifespan,
    # Disable documentation endpoints to add authentication later
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


##### Exception handling
@app.exception_handler(HTTPError)
async def http_exception_handler(request: Request, exc: HTTPError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(status=exc.status_code, message=str(exc)).model_dump(
            mode="json"
        ),
    )


##### Add routers
app.include_router(routers.health_router)
app.include_router(
    routers.organisation_router, dependencies=[Security(verify_endpoint_access)]
)
app.include_router(routers.user_router, dependencies=[Security(verify_endpoint_access)])


##### Add (possibly protected) documentation routes
@app.get(
    "/docs",
    include_in_schema=False,
    dependencies=[Depends(verify_documentation_access)],
)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Swagger UI",
    )


@app.get(
    "/redoc",
    include_in_schema=False,
    dependencies=[Depends(verify_documentation_access)],
)
async def get_redoc_documentation() -> HTMLResponse:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - ReDoc",
    )


@app.get(
    "/openapi.json",
    include_in_schema=False,
    dependencies=[Depends(verify_documentation_access)],
)
async def get_openapi_specification() -> dict[str, Any]:
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


##### Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
