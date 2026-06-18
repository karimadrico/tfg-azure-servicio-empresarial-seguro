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

El objetivo del TFG es demostrar una solución completa y evaluable: análisis del problema, diseño cloud, implementación, pruebas, despliegue, seguimiento de tareas en Zube y control de calidad con SonarCloud.

## Enlaces de evaluación

| Recurso | Enlace |
|---------|--------|
| Repositorio GitHub | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| Portal desplegado | https://app-tfg-incidencias-dev.azurewebsites.net/portal |
| API desplegada | https://app-tfg-incidencias-dev.azurewebsites.net |
| Zube (sprints y tablero Kanban) | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban |
| SonarCloud (calidad de código) | https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro |

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

Para ejecutar las pruebas automáticas desde la raíz del repositorio:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Despliegue en Azure (PowerShell)

```powershell
az login
.\scripts\deploy-azure.ps1
.\scripts\verify-azure.ps1
```

El despliegue publica la API y el portal en Azure App Service, configura el modo de almacenamiento cloud y permite validar el endpoint técnico `/health`.

## Calidad de Código

El repositorio incluye análisis de calidad con SonarCloud:

- Panel del proyecto: https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

- Configuración: `sonar-project.properties`
- Workflow: `.github/workflows/sonarcloud.yml`
- Guía: `docs/calidad/sonarcloud.md`

El workflow se ejecuta con cada push a `main` y realiza:

1. Instalación de dependencias Python.
2. Ejecución de pruebas unitarias.
3. Escaneo de calidad con SonarCloud.

Para que el análisis funcione en GitHub Actions debe existir el secreto `SONAR_TOKEN` en `Settings -> Secrets and variables -> Actions`.

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
- **SonarCloud (calidad):** https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro
- **Tribunal:** invitar usuario `ubutfgm`

## Entregables TFG

- `memoria/memoria.pdf`: memoria principal.
- `memoria/anexos.pdf`: anexos técnicos.
- `src/`: código fuente de la aplicación Flask y portal web.
- `tests/`: pruebas automáticas.
- `infra/terraform/` y `infra/bicep/`: infraestructura como código.
- `logicapp/`: definición del flujo de automatización.
- `docs/`: documentación de arquitectura, despliegue, decisiones, sprints y calidad.

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
