from fastapi import APIRouter, status

from repository_infrastructure_example.application.api.responses import (
    ErrorResponseModel,
    SuccessResponseModel,
)

health_router = APIRouter(prefix="/v1", tags=["health"])


@health_router.get(
    "/healthz",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponseModel,
            "description": "Service is healthy.",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponseModel,
            "description": "Service is unhealthy.",
        },
    },
)
def health() -> SuccessResponseModel:
    return SuccessResponseModel()
