# Especificación API REST

## 1. General

- Base URL: `https://tfg-servicio-empresarial.azurewebsites.net/`
- Versión: `1.0`
- Autenticación: identidades administradas de Azure con token Bearer.
- Formato de respuesta: `application/json`

---

## 2. Endpoints

### 2.1 GET `/`

Comprueba el estado del servicio.

Respuesta 200:
```json
{
  "mensaje": "API TFG Servicio Empresarial Seguro",
  "version": "1.0",
  "estado": "operacional",
  "timestamp": "2026-03-15T14:30:00Z"
}
```

Ejemplo:
```bash
curl https://tfg-servicio-empresarial.azurewebsites.net/
```

---

### 2.2 GET `/incidencias`

Obtiene el listado de incidencias.

Query parameters:

```text
estado: string (opcional) – Filtra por estado: abierta, en_proceso, cerrada.
prioridad: string (opcional) – Filtra por prioridad: baja, media, alta.
limit: integer (opcional) – Límite de resultados (por defecto: 50).
offset: integer (opcional) – Offset para paginación (por defecto: 0).
```

Respuesta 200:
```json
{
  "total": 3,
  "resultados": [
    {
      "id": "INC-001",
      "titulo": "Error en acceso a base de datos",
      "descripcion": "La aplicación no conecta con BD",
      "estado": "abierta",
      "prioridad": "alta",
      "clasificacion": "infraestructura",
      "fecha_creacion": "2026-03-15T10:00:00Z",
      "asignado_a": "soporte_equipo"
    }
  ]
}
```

Ejemplo:
```bash
curl "https://tfg-servicio-empresarial.azurewebsites.net/incidencias?estado=abierta&prioridad=alta"
```

Errores:

- `400 Bad Request`: parámetros inválidos.
- `401 Unauthorized`: no autenticado.
- `500 Internal Server Error`: error interno.

---

### 2.3 POST `/incidencias`

Crea una incidencia.

Headers:
```http
Content-Type: application/json
Authorization: Bearer <token>
```

Body:
```json
{
  "titulo": "Fallo en envío de emails",
  "descripcion": "Los emails de notificación no se envían",
  "prioridad": "alta",
  "reportado_por": "usuario@empresa.com",
  "categoria": "soporte"
}
```

Campos:

```text
titulo: string (requerido) – 1-200 caracteres.
descripcion: string (requerido) – 10-2000 caracteres.
prioridad: enum (opcional) – baja, media, alta. Defecto: media.
reportado_por: email (requerido) – email válido.
categoria: string (opcional) – soporte, feature_request, bug, seguridad.
```

Respuesta 201:
```json
{
  "id": "INC-003",
  "titulo": "Fallo en envío de emails",
  "descripcion": "Los emails de notificación no se envían",
  "estado": "abierta",
  "prioridad": "alta",
  "clasificacion_automatica": "infraestructura",
  "confianza_clasificacion": 0.87,
  "fecha_creacion": "2026-03-15T14:35:00Z",
  "fecha_vencimiento_estimada": "2026-03-16T14:35:00Z",
  "enlace_seguimiento": "/incidencias/INC-003"
}
```

Errores:

- `400 Bad Request`: datos inválidos.
- `401 Unauthorized`: no autenticado.
- `409 Conflict`: incidencia duplicada.
- `503 Service Unavailable`: servicio no disponible.

---

### 2.4 GET `/incidencias/{id}`

Obtiene los detalles de una incidencia.

Path parameter:

```text
id: string – Identificador de la incidencia, por ejemplo INC-001.
```

Respuesta 200:
```json
{
  "id": "INC-001",
  "titulo": "Error en acceso a base de datos",
  "descripcion": "La aplicación no conecta con BD",
  "estado": "abierta",
  "prioridad": "alta",
  "clasificacion": "infraestructura",
  "confianza_clasificacion": 0.92,
  "fecha_creacion": "2026-03-15T10:00:00Z",
  "fecha_ultima_actualizacion": "2026-03-15T12:00:00Z",
  "asignado_a": "soporte_equipo",
  "comentarios": [
    {
      "autor": "tech_lead@empresa.com",
      "texto": "Problema identificado en queries de conexión",
      "timestamp": "2026-03-15T11:30:00Z"
    }
  ],
  "historial_cambios": [
    {
      "campo_modificado": "estado",
      "valor_anterior": "nueva",
      "valor_nuevo": "abierta",
      "fecha": "2026-03-15T10:05:00Z",
      "usuario": "sistema"
    }
  ]
}
```

Errores:

- `404 Not Found`: incidencia no encontrada.
- `401 Unauthorized`: no autenticado.

---

### 2.5 PUT `/incidencias/{id}`

Actualiza los datos de una incidencia.

Path parameter:

```text
id: string – Identificador de la incidencia.
```

Body opcional:
```json
{
  "estado": "en_proceso",
  "prioridad": "media",
  "asignado_a": "nueva_persona@empresa.com",
  "comentario_interno": "Iniciando investigación"
}
```

Respuesta 200:
```json
{
  "id": "INC-001",
  "estado": "en_proceso",
  "fecha_ultima_actualizacion": "2026-03-15T14:40:00Z",
  "actualizado_por": "admin@empresa.com"
}
```

---

### 2.6 GET `/metricas`

Obtiene métricas del sistema.

Query parameter:

```text
periodo: string – hoy, semana, mes. Defecto: hoy.
```

Respuesta 200:
```json
{
  "total_incidencias": 15,
  "incidencias_abiertas": 6,
  "incidencias_en_proceso": 3,
  "incidencias_cerradas": 6,
  "tiempo_promedio_resolucion_horas": 4.5,
  "distribucion_por_prioridad": {
    "baja": 5,
    "media": 7,
    "alta": 3
  },
  "distribucion_por_clasificacion": {
    "infraestructura": 4,
    "soporte": 3,
    "feature_request": 5,
    "bug": 2,
    "seguridad": 1
  },
  "tasa_resolucion_24h": 0.73,
  "ultima_actualizacion": "2026-03-15T14:45:00Z"
}
```

Ejemplo:
```bash
curl "https://tfg-servicio-empresarial.azurewebsites.net/metricas?periodo=semana"
```

---

### 2.7 POST `/incidencias/{id}/clasificar`

Reclasifica una incidencia.

Path parameter:

```text
id: string – Identificador de la incidencia.
```

Body opcional:
```json
{
  "forzar_reclasificacion": true
}
```

Respuesta 200:
```json
{
  "id": "INC-001",
  "clasificacion_anterior": "infraestructura",
  "clasificacion_nueva": "base_datos",
  "confianza": 0.94,
  "razon": "Palabras clave: 'base de datos', 'conexión', 'queries'",
  "sugerencias_asignacion": [
    "dba_team@empresa.com",
    "infraestructura@empresa.com"
  ]
}
```

---

## 3. Códigos de estado HTTP

```text
200 OK – Solicitud exitosa.
201 Created – Recurso creado correctamente.
204 No Content – Operación exitosa sin contenido.
400 Bad Request – Datos inválidos en la solicitud.
401 Unauthorized – Credenciales inválidas o no proporcionadas.
403 Forbidden – Sin permisos suficientes.
404 Not Found – Recurso no encontrado.
409 Conflict – Conflicto de estado o recurso duplicado.
500 Internal Server Error – Error interno del servidor.
503 Service Unavailable – Servicio fuera de línea.
```

---

## 4. Autenticación y autorización

### 4.1 Identidades administradas (Azure)

Todas las solicitudes deben incluir el header:

```http
Authorization: Bearer <token>
```

Flujo de acceso:

1. La aplicación solicita un token a Azure Entra ID.
2. El cliente incluye el token en el header `Authorization`.
3. La API valida el token y comprueba permisos RBAC.
4. Si el acceso es válido, se procesa la solicitud.

### 4.2 Roles de acceso

```text
lector: GET /incidencias, GET /metricas
creador: POST /incidencias
editor: PUT /incidencias/{id}
admin: Todos los endpoints
```

---

## 5. Rate limiting

Límites:

- Usuarios autenticados: 1000 solicitudes por hora.
- Endpoints públicos: 100 solicitudes por hora.

Headers de control:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 2026-03-15T15:45:00Z
```

---

## 6. Ejemplo de consumo

```python
import os
import requests

API_URL = "https://tfg-servicio-empresarial.azurewebsites.net"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('AZURE_TOKEN')}"
}

payload = {
    "titulo": "Error en login",
    "descripcion": "Usuario no puede iniciar sesión",
    "prioridad": "alta",
    "reportado_por": "user@empresa.com",
    "categoria": "soporte"
}

response = requests.post(
    f"{API_URL}/incidencias",
    headers=headers,
    json=payload
)
response.raise_for_status()
print(response.json())
```

---

## 7. Documentación OpenAPI

Disponible en `GET /docs` y `GET /swagger.json`.

---

## 8. Notas

- No guardar credenciales en el código fuente.
- Usar Microsoft.Identity.Client o identidades administradas.
- Los errores deben devolver `error` y `codigo_error`.
- Utilizar timestamps ISO 8601 en UTC.
- Versión actual: `1.0`. `/v2/` planificada para futuras mejoras.

---

## 9. Historial de cambios

```text
1.0 | 2026-03-15 | Versión inicial con endpoints básicos
1.1 | Planificado | Autenticación OAuth2
2.0 | Planificado | Webhooks y eventos
```

