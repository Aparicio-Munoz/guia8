"""Pruebas funcionales de los endpoints users."""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_users_and_filters() -> None:
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) >= 3

    filtered = client.get("/users", params={"role": "support", "is_active": False})
    assert filtered.status_code == 200
    assert all(item["role"] == "support" and item["is_active"] is False for item in filtered.json())


def test_get_missing_user_returns_404() -> None:
    response = client.get("/users/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrado"}


def test_create_user_returns_201_and_rejects_duplicate_email() -> None:
    payload = {
        "name": "Usuario de Prueba",
        "email": "usuario.prueba@example.com",
        "role": "viewer",
        "is_active": True,
    }
    created = client.post("/users", json=payload)
    assert created.status_code == 201
    assert created.json()["email"] == payload["email"]

    duplicated = client.post("/users", json=payload)
    assert duplicated.status_code == 400
    assert duplicated.json()["detail"] == "El correo electrónico ya está registrado"


def test_invalid_payload_returns_422() -> None:
    response = client.post(
        "/users",
        json={"name": "A", "email": "no-es-un-correo", "role": "manager", "is_active": "yes"},
    )
    assert response.status_code == 422


def test_disallowed_role_returns_400() -> None:
    response = client.post(
        "/users",
        json={
            "name": "Rol Inválido",
            "email": "rol.invalido@example.com",
            "role": "manager",
            "is_active": True,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Rol no permitido"


def test_put_replaces_all_fields() -> None:
    payload = {
        "name": "Ana García Actualizada",
        "email": "ana.actualizada@example.com",
        "role": "operator",
        "is_active": False,
    }
    response = client.put("/users/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["is_active"] is False


def test_put_rejects_duplicate_email() -> None:
    response = client.put(
        "/users/1",
        json={
            "name": "Correo Duplicado",
            "email": "carlos.rodriguez@example.com",
            "role": "viewer",
            "is_active": True,
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El correo electrónico ya está registrado"


def test_patch_is_partial_and_cannot_be_empty() -> None:
    response = client.patch("/users/2", json={"role": "support"})
    assert response.status_code == 200
    assert response.json()["role"] == "support"

    empty = client.patch("/users/2", json={})
    assert empty.status_code == 400
    assert empty.json()["detail"] == "Debe enviar al menos un campo para actualizar"


def test_delete_returns_204_and_missing_delete_returns_404() -> None:
    created = client.post(
        "/users",
        json={
            "name": "Usuario Eliminable",
            "email": "eliminable@example.com",
            "role": "viewer",
            "is_active": True,
        },
    )
    user_id = created.json()["id"]
    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.delete(f"/users/{user_id}")
    assert missing.status_code == 404
