# Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información del servicio |
| GET | `/portal` | Portal web |
| GET | `/health` | Comprobación de salud |
| POST | `/solicitudes` | Crear solicitud |
| GET | `/solicitudes` | Listar solicitudes |
| GET | `/solicitudes/<id>` | Consultar detalle e historial |
| PATCH | `/solicitudes/<id>` | Gestionar estado, prioridad, asignación y notas |
| GET | `/metricas` | Métricas agregadas y SLA |

Los endpoints `GET /solicitudes` y `GET /metricas` requieren:

```http
Authorization: Bearer <token>
```
