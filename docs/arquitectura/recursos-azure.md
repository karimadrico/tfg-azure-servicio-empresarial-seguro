# Recursos Azure del proyecto

**Suscripción:** Azure for Students  
**Resource Group:** `rg-tfg-cloudautomation-dev`  
**Región principal:** Sweden Central

## Recursos desplegados

| Tipo | Nombre | Región | Uso |
|------|--------|--------|-----|
| App Service | `app-tfg-incidencias-dev` | Sweden Central | API Flask y portal web |
| App Service Plan | `ASP-rgtfgcloudautomationdev-b089` | Sweden Central | Plan de hospedaje |
| Storage Account | `sttfgincidenciasdev` | Sweden Central | Persistencia Blob de solicitudes |
| Key Vault | `kv-tfg-incidencias-dev` | Sweden Central | Secreto `api-key` |
| Managed Identity | Identidad del App Service | Sweden Central | Acceso seguro a Key Vault |

## URLs

- API: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net
- Portal: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
- Health: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health

