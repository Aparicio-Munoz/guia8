"""Modelos Pydantic para el recurso users."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StrictBool


UserRole = Literal["admin", "operator", "support", "viewer"]


class UserBase(BaseModel):
    """Campos compartidos por las operaciones de usuarios."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario.",
        examples=["María López"],
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico único del usuario.",
        examples=["maria.lopez@example.com"],
    )
    role: str = Field(
        ...,
        min_length=1,
        description="Rol asignado al usuario.",
        examples=["support"],
    )
    is_active: StrictBool = Field(
        ...,
        description="Indica si el usuario puede utilizar el sistema.",
        examples=[True],
    )


class UserCreate(UserBase):
    """Datos requeridos para crear un usuario."""


class UserPut(UserBase):
    """Datos requeridos para reemplazar completamente un usuario."""


class UserPatch(BaseModel):
    """Campos opcionales para actualizar parcialmente un usuario."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=2, max_length=100, examples=["María López"])
    email: EmailStr | None = Field(default=None, examples=["maria.lopez@example.com"])
    role: str | None = Field(default=None, min_length=1, examples=["support"])
    is_active: StrictBool | None = Field(default=None, examples=[True])


class UserResponse(UserBase):
    """Representación pública de un usuario."""

    id: int = Field(..., description="Identificador único del usuario.", examples=[1])
