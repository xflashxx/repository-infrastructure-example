from typing import Any
from uuid import UUID

from fastapi import status
from pydantic import BaseModel, Field

from repository_infrastructure_example.exceptions import HTTPError


class SuccessResponseModel(BaseModel):
    status: str = Field(default="ok", description="Status of the response.")


class ErrorResponseModel(BaseModel):
    status: int = Field(default=..., description="Status of the response.")
    message: str = Field(default=..., description="Error message.")


class ResourceCreatedResponseModel(BaseModel):
    id: UUID = Field(
        description="Unique identifier of the created object.",
        examples=["a1a5b075-b59a-4bc8-a567-d036aa1c547b"],
    )
    message: str = Field(
        description="Success message indicating the resource was created successfully.",
        examples=["Resource created successfully."],
    )


def openapi_responses_from_http_errors(
    *excs: type[HTTPError],
) -> dict[int, dict[str, Any]]:
    """
    Construct responses for FastAPI endpoints.

    :param exceptions: Exception classes to construct responses for.
    :return: Dictionary of FastAPI response definitions.
    """
    # Group exceptions by status code
    exceptions_by_status_code: dict[int, list[type[HTTPError]]] = dict()

    for exc in excs:
        if exc.status_code not in exceptions_by_status_code:
            exceptions_by_status_code[exc.status_code] = []
        exceptions_by_status_code[exc.status_code].append(exc)

    # Construct responses

    # Add default 500 response
    responses: dict[int, dict[str, Any]] = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": ErrorResponseModel,
            "description": "Internal Server Error.",
        }
    }

    for status_code, exceptions in exceptions_by_status_code.items():
        messages = [exc.detail for exc in exceptions]
        # Remove punctuation from messages
        messages = [message.rstrip(".") for message in messages]
        # Construct response description
        description = ", or ".join(messages)
        # Construct response model
        responses[status_code] = {
            "model": ErrorResponseModel,
            "description": description,
        }

    return responses
