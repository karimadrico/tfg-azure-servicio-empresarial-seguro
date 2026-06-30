# Recursos Azure del proyecto

**Suscripción:** Azure for Students  
**Resource Group:** `rg-tfg-cloudautomation-dev`  
**Región principal:** Sweden Central

## Recursos desplegados

| Tipo | Nombre | Región | Uso |
|------|--------|--------|-----|
| App Service | `app-tfg-incidencias-dev` | Sweden Central | API Flask y portal web. |
| App Service Plan | `ASP-rgtfgcloudautomationdev-b089` | Sweden Central | Plan de hospedaje Linux para App Service. |
| Azure Cosmos DB | `cosmos-tfg-kdr-2026` | Sweden Central | Persistencia documental final de solicitudes. |
| Cosmos DB database | `tfg-solicitudes` | Sweden Central | Base de datos NoSQL del prototipo. |
| Cosmos DB container | `solicitudes` | Sweden Central | Documentos JSON particionados por `/tipo_solicitud`. |
| Storage Account | `sttfgincidenciasdev` | Sweden Central | Persistencia inicial y origen de migración a Cosmos DB. |
| Key Vault | `kv-tfg-incidencias-dev` | Sweden Central | Secreto `api-key`. |
| Managed Identity | Identidad del App Service | Sweden Central | Acceso seguro desde App Service a Key Vault. |
| Logic App | `logic-tfg-solicitudes-dev` | Sweden Central | Entrada HTTP desde sistemas externos hacia la API. |
| Application Insights | `appi-tfg-incidencias-dev` | Sweden Central | Telemetría y observabilidad básica del servicio. |

## URLs públicas

- API: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net
- Portal: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
- Health: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health
- Ayuda: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/ayuda
- OpenAPI: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/docs

## Evidencias

Las capturas principales se encuentran en `docs/evidencias/`: Resource Group, App Service, configuración, Key Vault, Managed Identity, Cosmos DB, Logic App, Application Insights, SonarCloud y portal funcional.
