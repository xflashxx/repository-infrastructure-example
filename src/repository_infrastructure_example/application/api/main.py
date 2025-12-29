from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Security
from fastapi.responses import JSONResponse

from repository_infrastructure_example import __appname__, __version__
from repository_infrastructure_example.application.api import routers
from repository_infrastructure_example.application.api.authentication.api_key import (
    api_key_dependency,
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
    context.postgres_client.run_migrations()

    # Store application context
    app.state.context = context

    # Yield control to the application
    yield


# Create the FastAPI application
app = FastAPI(title=__appname__, version=__version__, lifespan=lifespan)


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
    routers.organisation_router, dependencies=[Security(api_key_dependency)]
)
app.include_router(routers.user_router, dependencies=[Security(api_key_dependency)])
