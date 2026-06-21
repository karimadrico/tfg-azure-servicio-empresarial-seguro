# Especificación API REST

## Información general

- Base URL: `https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net`
- Formato: JSON.
- Autenticación: token Bearer para endpoints de consulta.
- Persistencia: Azure Blob Storage en despliegue cloud y fichero JSON en local.

## Endpoints disponibles

| Método | Ruta | Protección | Descripción |
|--------|------|------------|-------------|
| GET | `/` | No | Información básica del servicio |
| GET | `/portal` | No | Portal web de solicitudes |
| GET | `/health` | No | Estado técnico y modo de almacenamiento |
| POST | `/solicitudes` | No | Crear solicitud TI |
| GET | `/solicitudes` | Bearer token | Listar solicitudes con filtros |
| GET | `/solicitudes/<id>` | Bearer token | Consultar detalle e historial |
| PATCH | `/solicitudes/<id>` | Bearer token | Actualizar estado, prioridad, responsable o nota |
| POST | `/incidencias` | No | Alias compatible para crear incidencia |
| GET | `/incidencias` | Bearer token | Alias compatible para listar incidencias |
| GET | `/metricas` | Bearer token | Métricas agregadas |

## Crear solicitud

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Necesito acceso VPN al entorno cloud","reportado_por":"usuario@empresa.com"}'
```

Campos principales:

| Campo | Obligatorio | Descripción |
|-------|-------------|-------------|
| `tipo_solicitud` | Sí | `acceso`, `entorno`, `aplicacion`, `configuracion` o `incidencia` |
| `titulo` | Sí | Resumen de la solicitud |
| `descripcion` | Sí | Detalle de la solicitud, entre 10 y 2000 caracteres |
| `reportado_por` | Sí | Email del solicitante |
| `prioridad` | No | `baja`, `media` o `alta`; si no se indica, se calcula |

## Consultar solicitudes

```powershell
$headers = @{ Authorization = "Bearer $env:API_KEY" }
Invoke-RestMethod `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -Headers $headers
```

Filtros opcionales:

- `estado`: `abierta`, `en_proceso`, `cerrada`.
- `prioridad`: `baja`, `media`, `alta`.
- `tipo_solicitud`: tipo soportado por el clasificador.
- `limit` y `offset`: paginación.

## Métricas

```powershell
Invoke-RestMethod `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/metricas" `
  -Headers $headers
```

Devuelve totales por prioridad, estado y tipo de solicitud. También incluye el bloque `sla`, con solicitudes `en_plazo`, `vencidas` y `cerradas`.

## Gestionar una solicitud

```powershell
Invoke-RestMethod `
  -Method PATCH `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes/SOL-001" `
  -Headers $headers `
  -ContentType "application/json" `
  -Body '{"estado":"en_proceso","asignado_a":"equipo_seguridad","comentario":"Identidad validada","actor":"operador@empresa.com"}'
```

Estados soportados: `abierta`, `en_proceso` y `cerrada`. Cada cambio se registra en `historial` junto con su fecha, actor y detalle.

