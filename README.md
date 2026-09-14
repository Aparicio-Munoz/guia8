# device_systems

API REST desarrollada con FastAPI para administrar usuarios de un sistema de dispositivos. La API permite consultar, crear, actualizar y eliminar usuarios, aplicar filtros por rol y estado, validar los datos recibidos y consultar la documentación interactiva de OpenAPI.

Los datos se almacenan temporalmente en una lista en memoria; por eso se reinician cada vez que se detiene el servidor.

## Tecnologías utilizadas

- Python 3.10 o superior.
- FastAPI para construir la API REST.
- Uvicorn como servidor ASGI.
- Pydantic v2 para esquemas y validación de datos.
- Pytest y HTTPX para las pruebas funcionales.
- OpenAPI, Swagger UI y ReDoc para la documentación automática.

## Instalación de dependencias

Desde la carpeta raíz del proyecto, crea y activa un entorno virtual e instala las dependencias:

```bash
python -m venv venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows
pip install -r requirements.txt
```

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`.

Enlaces de documentación:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Especificación OpenAPI: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## Endpoints

| Método | Ruta | Descripción | Respuesta exitosa |
|---|---|---|---:|
| GET | `/` | Comprueba que la API está disponible. | 200 |
| GET | `/users` | Lista todos los usuarios. | 200 |
| GET | `/users/{user_id}` | Consulta un usuario por su ID. | 200 |
| POST | `/users` | Crea un usuario nuevo. | 201 |
| PUT | `/users/{user_id}` | Reemplaza todos los campos de un usuario. | 200 |
| PATCH | `/users/{user_id}` | Actualiza únicamente los campos enviados. | 200 |
| DELETE | `/users/{user_id}` | Elimina un usuario. | 204 |

### Filtros de `GET /users`

La consulta acepta los parámetros opcionales `role` e `is_active`:

```text
GET /users?role=support&is_active=true
```

Los roles permitidos son `admin`, `operator`, `support` y `viewer`.

## Ejemplos de peticiones y respuestas

Los siguientes ejemplos usan `curl`. También pueden ejecutarse desde Swagger UI con el botón **Try it out**.

### Consultar usuarios

Petición:

```bash
curl http://127.0.0.1:8000/users
```

Respuesta `200 OK`:

```json
[
  {
    "id": 1,
    "name": "Ana García",
    "email": "ana.garcia@example.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Carlos Rodríguez",
    "email": "carlos.rodriguez@example.com",
    "role": "operator",
    "is_active": true
  }
]
```

### Filtrar usuarios

Petición:

```bash
curl "http://127.0.0.1:8000/users?role=support&is_active=false"
```

Respuesta `200 OK`:

```json
[
  {
    "id": 3,
    "name": "Luisa Martínez",
    "email": "luisa.martinez@example.com",
    "role": "support",
    "is_active": false
  }
]
```

### Consultar un usuario

```bash
curl http://127.0.0.1:8000/users/1
```

Respuesta `200 OK`:

```json
{
  "id": 1,
  "name": "Ana García",
  "email": "ana.garcia@example.com",
  "role": "admin",
  "is_active": true
}
```

### Crear un usuario — `POST /users`

Petición:

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María López",
    "email": "maria.lopez@example.com",
    "role": "support",
    "is_active": true
  }'
```

Respuesta `201 Created`:

```json
{
  "id": 4,
  "name": "María López",
  "email": "maria.lopez@example.com",
  "role": "support",
  "is_active": true
}
```

### Actualizar completamente un usuario — `PUT /users/1`

Todos los campos son obligatorios:

```bash
curl -X PUT http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ana García Actualizada",
    "email": "ana.actualizada@example.com",
    "role": "operator",
    "is_active": false
  }'
```

Respuesta `200 OK`:

```json
{
  "id": 1,
  "name": "Ana García Actualizada",
  "email": "ana.actualizada@example.com",
  "role": "operator",
  "is_active": false
}
```

### Actualizar parcialmente un usuario — `PATCH /users/1`

Solo se envían los campos que se desean modificar:

```bash
curl -X PATCH http://127.0.0.1:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"role": "support"}'
```

Respuesta `200 OK`:

```json
{
  "id": 1,
  "name": "Ana García Actualizada",
  "email": "ana.actualizada@example.com",
  "role": "support",
  "is_active": false
}
```

### Eliminar un usuario — `DELETE /users/1`

```bash
curl -i -X DELETE http://127.0.0.1:8000/users/1
```

Respuesta `204 No Content`: no contiene cuerpo.

## Códigos de estado usados

| Código | Significado y uso |
|---:|---|
| 200 | Consulta o actualización realizada correctamente. |
| 201 | Usuario creado correctamente. |
| 204 | Usuario eliminado correctamente; la respuesta no tiene cuerpo. |
| 400 | Regla de negocio incumplida: correo duplicado, rol no permitido o `PATCH` vacío. |
| 404 | No existe un usuario con el ID solicitado. |
| 422 | Los datos o parámetros no cumplen las validaciones de Pydantic/FastAPI. |

Ejemplo de error `404` o `400`:

```json
{
  "detail": "Usuario no encontrado"
}
```

## Uso de `Depends()`

`Depends()` permite declarar dependencias que FastAPI ejecuta e inyecta automáticamente antes de llamar a una ruta.

En este proyecto, `get_user_or_404` recibe el `user_id`, busca el usuario en la lista en memoria y genera un `404` si no existe. Se reutiliza en los endpoints GET por ID, PUT, PATCH y DELETE:

```python
def patch_user(
    user_data: UserPatch,
    user: UserRecord = Depends(get_user_or_404),
) -> UserRecord:
    ...
```

De esta forma, las rutas no repiten la búsqueda ni el manejo del error. También se inyecta `get_api_config` en `GET /users` como ejemplo de configuración compartida.

## Capturas de Swagger UI

Para tomar las capturas:

1. Instala las dependencias y ejecuta el servidor con `uvicorn app.main:app --reload`.
2. Abre [Swagger UI](http://127.0.0.1:8000/docs) en el navegador.
3. Toma una captura de la vista general donde se vean el título `device_systems API` y los endpoints.
4. Abre `POST /users`, pulsa **Try it out**, completa el JSON de ejemplo, pulsa **Execute** y captura la petición y la respuesta `201`.
5. Abre `GET /users/{user_id}`, usa el valor `1`, pulsa **Execute** y captura la respuesta `200`.
6. Guarda las imágenes en `docs/screenshots/` con estos nombres:

   - `swagger-overview.png`
   - `swagger-post-user.png`
   - `swagger-get-user.png`

En macOS puedes usar `Shift + Command + 4` para seleccionar un área o `Shift + Command + 5` para capturar una ventana. En Windows, usa `Win + Shift + S`; en Linux, la herramienta de capturas de tu entorno de escritorio.

Después de guardarlas, puedes mostrarlas en este README agregando:

```markdown
![Vista general de Swagger UI](docs/screenshots/swagger-overview.png)
![POST /users ejecutado en Swagger UI](docs/screenshots/swagger-post-user.png)
![GET /users/{user_id} ejecutado en Swagger UI](docs/screenshots/swagger-get-user.png)
```

## Pruebas

Para ejecutar las pruebas funcionales:

```bash
pytest -q
```

Las pruebas cubren listado, filtros, consulta inexistente, creación, correo duplicado, datos inválidos, PUT, PATCH, DELETE y las validaciones de negocio.
