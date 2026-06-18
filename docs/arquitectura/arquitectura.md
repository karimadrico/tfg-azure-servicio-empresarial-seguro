# Arquitectura del Sistema

## Descripción general

El sistema implementa una plataforma cloud para gestionar solicitudes internas de TI en Microsoft Azure. La solución está compuesta por un portal web, una API Flask, un clasificador ligero, almacenamiento en Azure Blob Storage y gestión segura de secretos con Azure Key Vault.

## Componentes principales

### Azure App Service

- Aloja la API Flask y el portal web.
- Ejecuta Gunicorn como servidor WSGI.
- Expone los endpoints `/`, `/portal`, `/health`, `/solicitudes` y `/metricas`.

### Azure Key Vault

- Almacena el secreto `api-key`.
- Evita credenciales en el código fuente.
- Se consulta desde la aplicación mediante Managed Identity.

### Azure Blob Storage

- Persiste las solicitudes en el contenedor `incidencias`.
- Permite conservar el histórico de solicitudes creadas durante la demo.

### Clasificador ligero

- Analiza título, descripción y tipo de solicitud.
- Calcula prioridad, categoría, recomendación y confianza.
- No depende de servicios de IA de pago.

## Flujo principal

```text
Usuario
  -> Portal web o API REST
  -> Validación de entrada
  -> Clasificación automática
  -> Persistencia en Blob Storage
  -> Respuesta JSON con prioridad y recomendación
```

## Seguridad

- HTTPS en App Service.
- Token Bearer en operaciones de consulta.
- Secreto en Key Vault.
- Managed Identity para acceso al secreto.
- Blob Storage privado.

## Despliegue

El despliegue operativo se realiza mediante `scripts/deploy-azure.ps1`, que configura identidad administrada, permisos de Key Vault, variables de entorno y publicación ZIP de `src/`.

