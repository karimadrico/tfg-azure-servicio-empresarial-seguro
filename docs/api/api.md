# Especificación API REST

## Información general

- Base URL: `https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net`.
- Formato principal: JSON.
- Contrato: OpenAPI 3.0 en `/openapi.json`.
- Explorador interactivo: Swagger UI en `/docs`.
- Autenticación interna: cabecera Bearer con secreto almacenado en Key Vault.
- Persistencia: Azure Cosmos DB en cloud, Azure Blob Storage como modo anterior/migración y fichero JSON en local.

## Registro de solicitudes

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "$baseUrl/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Acceso temporal para una auditoria","reportado_por":"usuario@empresa.com","servicio_id":"vpn","activo_id":"grupo-acceso-vpn","entorno":"produccion"}'
```

La API valida el contenido, aplica el clasificador ligero, resuelve servicio y activo, calcula impacto y SLA, determina si requiere aprobación y persiste el resultado.

## Gestión protegida

```powershell
$headers = @{ Authorization = "Bearer $env:API_KEY" }
Invoke-RestMethod -Uri "$baseUrl/solicitudes" -Headers $headers
```

Los filtros disponibles son `estado`, `prioridad`, `tipo_solicitud`, `servicio_id` e `impacto`. La paginación utiliza `limit` y `offset`.

Las transiciones, aprobaciones y escalados quedan registradas en el historial con fecha, actor y detalle. El centro operativo de `/operaciones` agrega carga por responsable, distribución por servicio, aprobaciones, alertas, vencimientos, resolución y satisfacción.

## Demostración

```powershell
Invoke-RestMethod -Method POST -Uri "$baseUrl/demo/cargar" -Headers $headers
```

La operación prepara cinco casos representativos. Es idempotente: una segunda ejecución informa de los registros existentes y no los duplica.

## Valoración

Una solicitud solo admite valoración después del cierre. El correo debe coincidir con el solicitante y se acepta una única respuesta entre uno y cinco puntos.

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "$baseUrl/solicitudes/SOL-001/valoracion" `
  -ContentType "application/json" `
  -Body '{"reportado_por":"usuario@empresa.com","puntuacion":5,"comentario":"Resolucion correcta"}'
```
