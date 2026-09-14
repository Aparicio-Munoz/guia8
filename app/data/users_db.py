"""Base de datos en memoria para fines académicos."""

from typing import Any


UserRecord = dict[str, Any]


users_db: list[UserRecord] = [
    {
        "id": 1,
        "name": "Ana García",
        "email": "ana.garcia@example.com",
        "role": "admin",
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Carlos Rodríguez",
        "email": "carlos.rodriguez@example.com",
        "role": "operator",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Luisa Martínez",
        "email": "luisa.martinez@example.com",
        "role": "support",
        "is_active": False,
    },
]


def get_next_user_id() -> int:
    """Obtiene un identificador incremental para un usuario nuevo."""

    return max((user["id"] for user in users_db), default=0) + 1
