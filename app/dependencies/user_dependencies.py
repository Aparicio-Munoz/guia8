"""Dependencias reutilizables para el recurso users."""

from fastapi import HTTPException, status

from app.data.users_db import UserRecord, users_db


API_CONFIG: dict[str, str] = {
    "name": "device_systems API",
    "version": "2.0.0",
}


def get_api_config() -> dict[str, str]:
    """Inyecta la configuración general disponible para las rutas."""

    return API_CONFIG


def get_user_or_404(user_id: int) -> UserRecord:
    """Busca un usuario por ID o detiene la petición con 404."""

    user = next((item for item in users_db if item["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


def validate_role_allowed(role: str) -> str:
    """Valida un rol desde una única función reutilizable."""

    allowed_roles = {"admin", "operator", "support", "viewer"}
    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol no permitido",
        )
    return role


def ensure_email_available(email: str, current_user_id: int | None = None) -> None:
    """Evita que dos usuarios compartan el mismo correo electrónico."""

    normalized_email = email.lower()
    duplicated = any(
        user["email"].lower() == normalized_email and user["id"] != current_user_id
        for user in users_db
    )
    if duplicated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado",
        )
