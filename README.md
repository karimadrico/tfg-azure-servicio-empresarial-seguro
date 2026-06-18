# Plataforma de Automatizacion de Solicitudes TI - TFG Azure

**Autora:** Karima Drafli Rico - Universidad de Burgos  
**Titulo:** Cloud Computing: Analisis, Diseno y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure

## Resumen

Este repositorio contiene el prototipo funcional del TFG: una plataforma cloud desplegada en Microsoft Azure para registrar, clasificar y consultar solicitudes internas de TI. La solucion incluye un portal web, una API Flask, clasificacion automatica ligera, persistencia en Azure Blob Storage, gestion segura de secretos con Azure Key Vault y despliegue reproducible mediante script PowerShell y Azure CLI.

El objetivo es demostrar una solucion completa y evaluable: analisis del problema empresarial, diseno cloud, implementacion, pruebas, despliegue real, seguimiento de tareas en Zube y control de calidad con SonarCloud.

## Enlaces de evaluacion

| Recurso | Enlace |
|---------|--------|
| Repositorio GitHub | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| Portal desplegado | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal |
| API desplegada | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net |
| Zube (sprints y Kanban) | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban |
| SonarCloud (calidad de codigo) | https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro |

## Arquitectura entregada

```text
Usuario / Tribunal
        |
        v
Portal web en Azure App Service
        |
        v
API Flask: solicitudes, incidencias, metricas y health check
        |
        +--> Clasificador ligero de solicitudes TI
        |
        +--> Azure Blob Storage: persistencia de incidencias
        |
        +--> Azure Key Vault: secreto de autenticacion
        |
        +--> Managed Identity: acceso seguro desde App Service
```

## Recursos Azure

| Recurso | Nombre |
|---------|--------|
| Resource Group | `rg-tfg-cloudautomation-dev` |
| App Service | `app-tfg-incidencias-dev` |
| Storage Account | `sttfgincidenciasdev` |
| Key Vault | `kv-tfg-incidencias-dev` |
| Region | `Sweden Central` |

## Prueba rapida

Comprobar estado:

```powershell
Invoke-RestMethod https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health
```

Abrir portal:

```powershell
Start-Process https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
```

Consultar solicitudes protegidas:

```powershell
Invoke-RestMethod `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -Headers @{ Authorization = "Bearer tfg-api-key-ubu-2026" }
```

Crear solicitud:

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Necesito acceso VPN al entorno cloud","reportado_por":"kdr1001@alu.ubu.es"}'
```

## Ejecucion local

```powershell
cd src
$env:STORAGE_MODE = "local"
pip install -r requirements.txt
python app.py
```

Abrir `http://localhost:5000/portal`.

## Pruebas

Desde la raiz del repositorio:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Despliegue en Azure

El despliegue real utilizado para el TFG se realiza desde PowerShell con Azure CLI:

```powershell
az login
.\scripts\deploy-azure.ps1
.\scripts\verify-azure.ps1
```

El script `scripts/deploy-azure.ps1`:

- comprueba sesion de Azure CLI;
- obtiene configuracion de Storage y Key Vault;
- habilita Managed Identity en App Service;
- concede acceso de App Service a Key Vault;
- guarda la clave de API como secreto;
- configura variables de entorno del App Service;
- publica la carpeta `src/` mediante despliegue ZIP.

## Calidad de codigo

La calidad se revisa manualmente en SonarCloud:

- Panel: https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro
- Puerta de calidad: aprobada.
- Duplicacion: 0,0%.
- Evidencia recomendada para entrega: captura del Quality Gate y resumen de metricas.

No se mantiene un workflow de SonarCloud en el repositorio porque el analisis se gestiona desde la interfaz web de SonarCloud.

## Endpoints principales

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Informacion basica del servicio |
| GET | `/portal` | Portal web empresarial |
| GET | `/health` | Estado tecnico del sistema |
| POST | `/solicitudes` | Crear solicitud TI |
| GET | `/solicitudes` | Listar solicitudes, protegido con Bearer token |
| GET | `/metricas` | Metricas agregadas, protegido con Bearer token |

## Estructura

```text
src/               API Flask, clasificador, almacenamiento y portal web
tests/             Pruebas unitarias
scripts/           Despliegue y verificacion en Azure
infra/terraform/   Infraestructura como codigo documentada
infra/bicep/       Plantillas Bicep alternativas/documentales
memoria/           Memoria y anexos LaTeX/PDF
docs/              Evidencias, arquitectura, despliegue, sprints y calidad
```

## Entregables TFG

- `memoria/memoria.pdf`: memoria principal.
- `memoria/anexos.pdf`: anexos tecnicos.
- Codigo fuente en `src/`.
- Pruebas en `tests/`.
- Evidencias y documentacion en `docs/`.
- Diagramas textuales en `docs/diagramas/diagramas.md`.
- Base del PDF de enlaces en `docs/entrega/enlaces-tfg.md`.
- Licencia MIT en `LICENSE`.
