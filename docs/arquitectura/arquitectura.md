# Arquitectura del Sistema

## Descripción general

El sistema implementa una plataforma cloud para gestionar solicitudes internas de TI en Microsoft Azure. La solución está compuesta por un portal web, una API Flask, un clasificador ligero, persistencia documental en Azure Cosmos DB y gestión segura de secretos con Azure Key Vault.

## Componentes principales

### Azure App Service

- Aloja la API Flask y el portal web.
- Ejecuta Gunicorn como servidor WSGI.
- Expone los endpoints `/`, `/portal`, `/health`, `/solicitudes` y `/metricas`.

### Azure Key Vault

- Almacena el secreto `api-key`.
- Evita credenciales en el código fuente.
- Se consulta desde la aplicación mediante Managed Identity.

### Azure Cosmos DB

- Persiste cada solicitud como documento JSON independiente.
- Utiliza la base de datos `tfg-solicitudes` y el contenedor `solicitudes`.
- Permite conservar histórico, estados, aprobaciones y valoraciones sin concentrar toda la colección en un único blob.

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
  -> Persistencia en Cosmos DB
  -> Respuesta JSON con prioridad y recomendación
```

## Seguridad

- HTTPS en App Service.
- Token Bearer en operaciones de consulta.
- Secreto en Key Vault.
- Managed Identity para acceso al secreto.
- Cosmos DB con contenedor privado y acceso desde la API.

## Despliegue

El despliegue operativo se realiza mediante `scripts/deploy-azure.ps1`, que configura identidad administrada, permisos de Key Vault, variables de entorno y publicación ZIP de `src/`.
