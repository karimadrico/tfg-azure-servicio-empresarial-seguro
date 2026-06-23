# Endpoints de la plataforma

La especificación ejecutable se publica en `/docs` y su contrato OpenAPI 3.0 en `/openapi.json`.

| Método | Endpoint | Protección | Descripción |
|--------|----------|------------|-------------|
| GET | `/` | Pública | Información y versión |
| GET | `/portal` | Pública | Portal empresarial |
| GET | `/ayuda` | Pública | Guía de uso |
| GET | `/acerca` | Pública | Arquitectura y enlaces |
| GET | `/health` | Pública | Salud y almacenamiento |
| GET | `/catalogo` | Pública | Servicios, activos y entornos |
| POST | `/solicitudes` | Pública | Registro y clasificación |
| GET | `/solicitudes` | Bearer | Listado filtrado y paginado |
| GET | `/solicitudes/<id>` | Bearer | Detalle e historial |
| PATCH | `/solicitudes/<id>` | Bearer | Estado, prioridad y asignación |
| POST | `/solicitudes/<id>/aprobacion` | Bearer | Decisión de aprobación |
| POST | `/solicitudes/<id>/escalar` | Bearer | Escalado trazable |
| POST | `/solicitudes/<id>/notificar-aprobacion` | Bearer | Evidencia de notificación |
| POST | `/solicitudes/<id>/valoracion` | Solicitante | Satisfacción tras el cierre |
| GET | `/metricas` | Bearer | Agregados de proceso y SLA |
| GET | `/operaciones` | Bearer | Carga, alertas y satisfacción |
| GET | `/informes/solicitudes.csv` | Bearer | Informe operativo CSV |
| POST | `/demo/cargar` | Bearer | Escenario demostrable idempotente |

Los endpoints protegidos requieren:

```http
Authorization: Bearer <token>
```
