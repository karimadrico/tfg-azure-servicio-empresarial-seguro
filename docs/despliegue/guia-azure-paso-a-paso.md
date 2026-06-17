# Guía rápida — Desplegar la plataforma en Azure

## Paso 0 — Requisitos

- Cuenta **Azure for Students** activa
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) instalado
- PowerShell en Windows

## Paso 1 — Login

```powershell
az login
az account set --subscription "Azure for Students"
az group show --name rg-tfg-cloudautomation-dev
```

Si el resource group no existe:

```powershell
az group create --name rg-tfg-cloudautomation-dev --location swedencentral
```

## Paso 2 — Desplegar API + configurar Storage y Key Vault

Desde la raíz del repositorio:

```powershell
cd "c:\Users\kdraf\OneDrive\Escritorio\TFG\tfg-azure-servicio-empresarial-seguro"
.\scripts\deploy-azure.ps1
```

Este script:
1. Configura **Managed Identity**
2. Guarda el **api-key** en Key Vault
3. Conecta **Blob Storage**
4. Publica el código de `src/` en App Service

## Paso 3 — Verificar que funciona

```powershell
.\scripts\verify-azure.ps1
```

O manualmente:

```powershell
$base = "https://app-tfg-incidencias-dev.azurewebsites.net"
$headers = @{ Authorization = "Bearer tfg-api-key-ubu-2026" }

Invoke-RestMethod "$base/health"
Invoke-RestMethod "$base/portal"   # abrir en navegador

Invoke-RestMethod -Method POST "$base/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Necesito acceso VPN al entorno de desarrollo cloud","reportado_por":"karima@ubu.es"}'

Invoke-RestMethod "$base/solicitudes" -Headers $headers
Invoke-RestMethod "$base/metricas" -Headers $headers
```

## Paso 4 — Crear Logic App en Portal Azure

1. Ir a [portal.azure.com](https://portal.azure.com)
2. **Create a resource** → **Logic App**
3. Nombre: `logic-tfg-solicitudes-dev`
4. Resource group: `rg-tfg-cloudautomation-dev`
5. Region: **Sweden Central**
6. Plan: **Consumption**
7. Abrir **Logic App Designer** → **Blank Logic App**
8. Trigger: **When a HTTP request is received**
9. Schema JSON:

```json
{
  "tipo_solicitud": "acceso",
  "titulo": "texto",
  "descripcion": "texto",
  "reportado_por": "email@empresa.com"
}
```

10. Acción: **HTTP** → POST  
    `https://app-tfg-incidencias-dev.azurewebsites.net/solicitudes`
11. Headers:
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer tfg-api-key-ubu-2026`
12. Body: contenido del trigger
13. Acción: **Response** → código 201, body = salida del HTTP
14. **Save** → copiar URL del trigger

## Paso 5 — Probar Logic App

```powershell
$logicUrl = "PEGAR_URL_DEL_TRIGGER"
$body = @{
  tipo_solicitud = "entorno"
  titulo = "Nuevo entorno staging"
  descripcion = "Solicito creacion de entorno staging para validar despliegue cloud"
  reportado_por = "karima@ubu.es"
} | ConvertTo-Json

Invoke-RestMethod -Method POST $logicUrl -ContentType "application/json" -Body $body
```

## Paso 6 — Commits y GitHub

```powershell
git add src/ logicapp/ infra/bicep/ docs/ README.md tests/
git commit -m "Plataforma de solicitudes TI con portal web, IA y Logic App"
git push origin main
```

## Paso 7 — Invitar al tribunal

En GitHub: Settings → Collaborators → añadir `ubutfgm`  
En Zube: invitar `ubutfgm`

## URLs para la memoria y el tribunal

| Recurso | URL |
|---------|-----|
| Repositorio | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| API | https://app-tfg-incidencias-dev.azurewebsites.net |
| Portal | https://app-tfg-incidencias-dev.azurewebsites.net/portal |
| Zube | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro |
