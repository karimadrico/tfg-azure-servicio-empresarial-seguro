# Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información del servicio |
| GET | `/portal` | Portal web |
| GET | `/health` | Comprobación de salud |
| POST | `/solicitudes` | Crear solicitud |
| GET | `/solicitudes` | Listar solicitudes |
| GET | `/metricas` | Métricas agregadas |

Los endpoints `GET /solicitudes` y `GET /metricas` requieren:

```http
Authorization: Bearer <token>
```

