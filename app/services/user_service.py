"""Reglas de negocio y operaciones sobre usuarios."""

from typing import Any

from app.data.users_db import UserRecord, get_next_user_id, users_db
from app.dependencies.user_dependencies import ensure_email_available, validate_role_allowed
from app.schemas.user_schema import UserCreate, UserPatch, UserPut


def list_users(role: str | None = None, is_active: bool | None = None) -> list[UserRecord]:
    """Lista usuarios, aplicando filtros opcionales."""

    return [
        user
        for user in users_db
        if (role is None or user["role"] == role)
        and (is_active is None or user["is_active"] == is_active)
    ]


def create_user(user_data: UserCreate) -> UserRecord:
    """Crea un usuario después de validar rol y correo."""

    validate_role_allowed(user_data.role)
    ensure_email_available(str(user_data.email))
    user = {"id": get_next_user_id(), **user_data.model_dump(mode="json")}
    users_db.append(user)
    return user


def replace_user(user: UserRecord, user_data: UserPut) -> UserRecord:
    """Reemplaza todos los campos editables de un usuario."""

    validate_role_allowed(user_data.role)
    ensure_email_available(str(user_data.email), current_user_id=user["id"])
    user.update(user_data.model_dump(mode="json"))
    return user


def update_user(user: UserRecord, changes: dict[str, Any]) -> UserRecord:
    """Actualiza únicamente los campos recibidos."""

    if "role" in changes:
        validate_role_allowed(changes["role"])
    if "email" in changes:
        ensure_email_available(str(changes["email"]), current_user_id=user["id"])
    user.update(changes)
    return user


def delete_user(user: UserRecord) -> None:
    """Elimina un usuario de la base en memoria."""

    users_db.remove(user)

