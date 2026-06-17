# Plataforma de Automatización de Solicitudes TI — TFG Azure

**Autora:** Karima Drafli Rico — Universidad de Burgos  
**Título:** Cloud Computing: Análisis, Diseño y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure

## Qué es

Plataforma cloud en Microsoft Azure para **automatizar solicitudes internas de TI** de una empresa:

1. El usuario envía una solicitud (acceso, entorno, aplicación, configuración o incidencia).
2. La **Logic App** orquesta el flujo.
3. La **API Flask** clasifica la solicitud con un componente de **IA ligera** (reglas + análisis semántico).
4. Se genera una **recomendación operativa** automática.
5. Los datos se almacenan en **Blob Storage** y los secretos en **Key Vault**.

## Arquitectura

```text
Portal Web (App Service)
        |
        v
Logic App (trigger HTTP)
        |
        +--> API Flask (clasificación IA + recomendación)
        |
        +--> Azure Blob Storage
        |
        +--> Azure Key Vault
        |
        +--> Notificación (email / respuesta JSON)
```

## Recursos Azure

| Recurso | Nombre |
|---------|--------|
| Resource Group | `rg-tfg-cloudautomation-dev` |
| App Service | `app-tfg-incidencias-dev` |
| Storage Account | `sttfgincidenciasdev` |
| Key Vault | `kv-tfg-incidencias-dev` |
| Logic App | `logic-tfg-solicitudes-dev` |

**URL API:** https://app-tfg-incidencias-dev.azurewebsites.net  
**Portal:** https://app-tfg-incidencias-dev.azurewebsites.net/portal

## Ejecución local

```powershell
cd src
$env:STORAGE_MODE = "local"
pip install -r requirements.txt
python app.py
```

Abrir http://localhost:5000/portal

## Despliegue en Azure (PowerShell)

```powershell
az login
.\scripts\deploy-azure.ps1
.\scripts\verify-azure.ps1
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/portal` | Portal web empresarial |
| GET | `/health` | Salud del sistema |
| POST | `/solicitudes` | Crear solicitud TI (público) |
| GET | `/solicitudes` | Listar solicitudes (auth) |
| GET | `/metricas` | Métricas agregadas (auth) |

## Repositorio y gestión

- **GitHub:** https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro
- **Zube (sprints):** https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban
- **Tribunal:** invitar usuario `ubutfgm`

## Estructura

```text
src/              API Flask + portal web
logicapp/         Logic App workflow.json
infra/terraform/  Infraestructura (Terraform)
infra/bicep/      Infraestructura alternativa (Bicep)
tests/            Pruebas unitarias
memoria/          Memoria LaTeX
docs/             Documentación
```
