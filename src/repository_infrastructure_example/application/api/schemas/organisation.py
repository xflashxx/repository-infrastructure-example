from pydantic import BaseModel, EmailStr, Field


class OrganisationCreateModel(BaseModel):
    name: str = Field(
        description="Name of the organisation.", examples=["Acme Inc."], min_length=3
    )
    email: EmailStr = Field(
        description="Email address of the organisation.", examples=["acme@acme.com"]
    )
    is_active: bool = Field(
        description="Whether the organisation is active.", examples=[True]
    )


class OrganisationUpdateModel(BaseModel):
    name: str | None = Field(
        default=None,
        description="Updated name of the organisation.",
        examples=["Acme Inc."],
        min_length=3,
    )
    email: EmailStr | None = Field(
        default=None,
        description="Updated email address of the organisation.",
        examples=["acme@acme.com"],
    )
    is_active: bool | None = Field(
        default=None,
        description="Updated status of the organisation.",
        examples=[True],
    )
