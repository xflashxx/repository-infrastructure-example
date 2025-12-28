from pydantic import BaseModel, EmailStr, Field


class UserCreateModel(BaseModel):
    first_name: str = Field(
        description="First name of the user.", examples=["John"], min_length=2
    )
    last_name: str = Field(
        description="Last name of the user.", examples=["Doe"], min_length=2
    )
    email: EmailStr = Field(
        description="Email address of the user.", examples=["john.doe@example.com"]
    )
    is_active: bool = Field(
        description="Whether the organisation is active.", examples=[True]
    )


class UserUpdateModel(BaseModel):
    first_name: str | None = Field(
        default=None,
        description="Updated first name of the user.",
        examples=["John"],
        min_length=2,
    )
    last_name: str | None = Field(
        default=None,
        description="Updated last name of the user.",
        examples=["Doe"],
        min_length=2,
    )
    email: EmailStr | None = Field(
        default=None,
        description="Updated email address of the user.",
        examples=["john.doe@example.com"],
    )
    is_active: bool | None = Field(
        default=None,
        description="Updated status of the user.",
        examples=[True],
    )
