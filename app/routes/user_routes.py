"""Endpoints REST para la gestión de usuarios."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.data.users_db import UserRecord
from app.dependencies.user_dependencies import get_api_config, get_user_or_404
from app.schemas.user_schema import UserCreate, UserPatch, UserPut, UserResponse, UserRole
from app.services import user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por rol y estado de actividad.",
    response_description="Lista de usuarios que coincide con los filtros.",
)
def get_users(
    role: UserRole | None = Query(default=None, description="Filtra por rol permitido."),
    is_active: bool | None = Query(default=None, description="Filtra por estado activo."),
    config: dict[str, str] = Depends(get_api_config),
) -> list[UserRecord]:
    """Lista usuarios con filtros opcionales."""

    _ = config
    return user_service.list_users(role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario",
    description="Busca un usuario por su identificador único.",
    response_description="Usuario encontrado.",
)
def get_user(user: UserRecord = Depends(get_user_or_404)) -> UserRecord:
    """Retorna el usuario resuelto por la dependencia get_user_or_404."""

    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un usuario nuevo con correo único y un rol permitido.",
    response_description="Usuario creado correctamente.",
)
def create_user(user_data: UserCreate) -> UserRecord:
    """Crea un usuario."""

    return user_service.create_user(user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente",
    description="Reemplaza todos los campos del usuario. Todos los campos son obligatorios.",
    response_description="Usuario reemplazado correctamente.",
)
def replace_user(
    user_data: UserPut,
    user: UserRecord = Depends(get_user_or_404),
) -> UserRecord:
    """Reemplaza por completo un usuario existente."""

    return user_service.replace_user(user, user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente",
    description="Modifica solo los campos enviados. Debe enviarse al menos un campo.",
    response_description="Usuario actualizado parcialmente.",
)
def patch_user(
    user_data: UserPatch,
    user: UserRecord = Depends(get_user_or_404),
) -> UserRecord:
    """Actualiza parcialmente un usuario."""

    changes: dict[str, Any] = user_data.model_dump(exclude_unset=True, mode="json")
    if not changes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )
    return user_service.update_user(user, changes)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente y no retorna contenido en la respuesta.",
    response_description="Usuario eliminado correctamente.",
)
def delete_user(user: UserRecord = Depends(get_user_or_404)) -> Response:
    """Elimina un usuario y retorna 204 No Content."""

    user_service.delete_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
