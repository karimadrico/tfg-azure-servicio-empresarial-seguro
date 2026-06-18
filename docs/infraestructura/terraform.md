# Infraestructura como código

El repositorio mantiene definiciones Terraform en `infra/terraform/` y plantillas Bicep en `infra/bicep/` para documentar la infraestructura Azure del proyecto.

## Recursos descritos

| Recurso | Uso |
|---------|-----|
| Resource Group | Contenedor lógico de la solución |
| App Service Plan | Plan Linux para la aplicación |
| Web App | API Flask y portal web |
| Storage Account | Persistencia de solicitudes |
| Blob Container | Contenedor privado `incidencias` |
| Key Vault | Secreto `api-key` |
| Managed Identity | Acceso seguro de App Service a Key Vault |
| RBAC de Key Vault | Roles `Key Vault Secrets Officer` y `Key Vault Secrets User` |
| Application Insights | Telemetría del App Service y apoyo a observabilidad |

## Uso recomendado

Terraform y Bicep se conservan como documentación reproducible y punto de partida para recrear la infraestructura. El despliegue operativo final del TFG se realiza con:

```powershell
.\scripts\deploy-azure.ps1
```

Ese script configura además aspectos de ejecución que son necesarios para la demo: variables de entorno, secreto en Key Vault, permisos de Managed Identity y publicación ZIP de la carpeta `src/`.

