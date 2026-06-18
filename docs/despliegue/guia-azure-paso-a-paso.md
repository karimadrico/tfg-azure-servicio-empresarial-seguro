# Guía rápida de despliegue en Azure

## Requisitos

- Cuenta Azure for Students activa.
- Azure CLI instalado.
- PowerShell en Windows.
- Recursos Azure creados en el grupo `rg-tfg-cloudautomation-dev`.

## Login

```powershell
az login
az account set --subscription "Azure for Students"
az group show --name rg-tfg-cloudautomation-dev
```

## Despliegue

Desde la raíz del repositorio:

```powershell
.\scripts\deploy-azure.ps1
```

El script realiza:

1. Comprobación de sesión en Azure CLI.
2. Lectura de Storage Account y Key Vault.
3. Activación de Managed Identity en App Service.
4. Asignación de permisos de Key Vault.
5. Creación/actualización del secreto `api-key`.
6. Configuración de variables de entorno del App Service.
7. Publicación ZIP del contenido de `src/`.

## Verificación

```powershell
.\scripts\verify-azure.ps1
```

## Despliegue de Logic App

```powershell
$env:API_KEY = "<clave usada en Key Vault>"
.\scripts\deploy-logicapp.ps1
```

Despues del despliegue, abrir `logic-tfg-solicitudes-dev` en Azure Portal, entrar en el trigger HTTP y copiar la URL de invocacion para probar el flujo.

Comprobación manual:

```powershell
$base = "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net"
$headers = @{ Authorization = "Bearer $env:API_KEY" }

Invoke-RestMethod "$base/health"
Start-Process "$base/portal"

Invoke-RestMethod -Method POST "$base/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Necesito acceso VPN al entorno de desarrollo cloud","reportado_por":"karima@ubu.es"}'

Invoke-RestMethod "$base/solicitudes" -Headers $headers
Invoke-RestMethod "$base/metricas" -Headers $headers
```

## URLs para tribunal

| Recurso | URL |
|---------|-----|
| Repositorio | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| API | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net |
| Portal | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal |
| SonarCloud | https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro |
| Zube | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban |

