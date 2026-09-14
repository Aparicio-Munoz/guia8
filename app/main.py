"""Punto de entrada de la API device_systems."""

from fastapi import FastAPI

from app.routes.user_routes import router as user_router


app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Incluye CRUD completo, validaciones, filtros y manejo profesional de errores."
    ),
    version="2.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "soporte@device-systems.example.com",
    },
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operaciones CRUD y consultas del recurso users.",
        }
    ],
)

app.include_router(user_router)


@app.get("/", include_in_schema=False, summary="Información de la API")
def root() -> dict[str, str]:
    """Indica que la API está disponible y enlaza a su documentación."""

    return {
        "name": "device_systems API",
        "version": "2.0.0",
        "message": "API disponible",
        "docs": "/docs",
        "redoc": "/redoc",
    }

