# Plataforma de Automatización de Solicitudes TI en Azure

**Autora:** Karima Drafli Rico  
**Titulación:** Grado en Ingeniería Informática Online, Universidad de Burgos  
**Título:** Cloud Computing: Análisis, Diseño y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure

Este repositorio contiene el prototipo funcional desarrollado para el Trabajo Fin de Grado. La solución automatiza la gestión de solicitudes internas de TI mediante un portal web, una API Flask desplegada en Azure App Service, persistencia documental en Azure Cosmos DB, gestión segura de secretos con Azure Key Vault, identidad administrada, Logic App para entrada desde sistemas externos y observabilidad con Application Insights.

El objetivo no es sustituir a una plataforma ITSM comercial, sino demostrar de extremo a extremo el análisis, diseño, implementación, despliegue, validación y documentación de una solución cloud empresarial segura en Microsoft Azure.

![Arquitectura integral del TFG en Microsoft Azure](memoria/img/arquitectura_integral_tfg_azure.png)

## Enlaces de evaluación

| Recurso | Enlace |
|---------|--------|
| Repositorio GitHub | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| Portal desplegado | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal |
| API desplegada | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net |
| Estado de la API | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health |
| Ayuda integrada | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/ayuda |
| Documentación OpenAPI | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/docs |
| Zube, sprints y Kanban | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban |
| SonarCloud | https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro |
| Release v1.1.0 | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro/releases/tag/v1.1.0 |

Las operaciones públicas permiten registrar solicitudes y consultar la ayuda. Las operaciones de equipo TI, métricas, exportación, carga de demostración y gestión interna requieren token Bearer. Ese token se facilita únicamente en el PDF de enlaces entregado en UBUVirtual y corresponde al secreto `api-key` almacenado en Azure Key Vault.

## Recorrido de demostración

| Paso | Pantalla o enlace | Qué se comprueba |
|------|-------------------|------------------|
| 1 | `/health` | La API responde `estado: ok` y confirma `storage_mode: cosmos`. |
| 2 | `/portal` | Registro de una solicitud sensible desde el portal web. |
| 3 | Resultado de solicitud | Clasificación, prioridad, impacto, responsable, SLA y estado inicial. |
| 4 | Gestión del equipo TI | Acceso protegido con token Bearer y filtrado de solicitudes. |
| 5 | Detalle de solicitud | Historial, catálogo de servicio/activo, aprobación y escalado. |
| 6 | Centro operativo | Carga por responsable, SLA vencido, métricas y satisfacción. |
| 7 | Exportación CSV | Generación de informe operativo protegido. |
| 8 | Logic App | Entrada automática desde un sistema externo mediante HTTP. |
| 9 | `/docs` | Contrato OpenAPI interactivo del servicio. |
| 10 | SonarCloud y Zube | Calidad del código, planificación por sprints y evidencias de proceso. |

## Prueba rápida

Abrir el portal:

```text
https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
```

Comprobar el estado desde PowerShell:

```powershell
Invoke-RestMethod `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health"
```

Consultar solicitudes protegidas:

```powershell
$env:API_KEY = "<token-de-evaluacion>"

Invoke-RestMethod `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -Headers @{ Authorization = "Bearer $env:API_KEY" }
```

Crear una solicitud desde PowerShell:

```powershell
Invoke-RestMethod `
  -Method POST `
  -Uri "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/solicitudes" `
  -ContentType "application/json" `
  -Body '{"tipo_solicitud":"acceso","titulo":"Acceso VPN","descripcion":"Necesito acceso VPN al entorno cloud","reportado_por":"usuario@empresa.com"}'
```

## Arquitectura

La arquitectura final se compone de los siguientes servicios y responsabilidades:

| Componente | Uso en el TFG |
|------------|---------------|
| Azure App Service | Aloja el portal web y la API Flask. |
| API Flask | Centraliza validación, catálogo, reglas de negocio, clasificación, aprobación, escalado, SLA e historial. |
| Azure Cosmos DB | Conserva cada solicitud como documento JSON independiente en el contenedor `solicitudes`. |
| Azure Key Vault | Almacena el token de autenticación fuera del código fuente. |
| Managed Identity | Permite que App Service acceda a Key Vault sin credenciales cloud embebidas. |
| Azure Logic Apps | Recibe solicitudes desde sistemas externos y llama a `POST /solicitudes`. |
| Application Insights / Azure Monitor | Recoge telemetría básica y facilita la observabilidad del despliegue. |
| Zube | Documenta la planificación ágil en cinco sprints cerrados. |
| SonarCloud | Aporta análisis externo de calidad, seguridad, fiabilidad y mantenibilidad. |

## Funcionalidades implementadas

- Portal web para registrar solicitudes de acceso, configuración, soporte e incidencias.
- Catálogo de servicios, activos, entornos, criticidad, propietario técnico y aprobador.
- Clasificación ligera y explicable de solicitudes TI.
- Cálculo de prioridad, impacto, SLA y equipo responsable.
- Bandeja protegida para el equipo TI.
- Aprobación y rechazo de solicitudes sensibles.
- Escalado, cierre y valoración final de solicitudes.
- Historial completo de eventos por solicitud.
- Centro operativo con métricas, SLA, carga y satisfacción.
- Exportación CSV de solicitudes.
- Documentación OpenAPI integrada.
- Logic App para automatizar la entrada desde sistemas externos.

## Calidad y validación

El proyecto incluye validación técnica y evidencias de calidad:

| Evidencia | Estado |
|-----------|--------|
| Pruebas automáticas | 27 pruebas superadas con `unittest`. |
| SonarCloud | Quality Gate aprobado en el análisis final documentado. |
| Duplicación | 0,0 % en el análisis de calidad documentado. |
| Seguridad | Endpoints internos protegidos con Bearer token y secreto almacenado en Key Vault. |
| Despliegue | API y portal desplegados en Azure App Service. |
| Verificación | Script `scripts/verify-azure.ps1` para comprobar `/health`, solicitudes, métricas y portal. |

![Quality Gate final aprobado en SonarCloud](docs/evidencias/sonarcloud-quality-gate-final-30junio.png)

## Ejecución local

```powershell
cd src
$env:STORAGE_MODE = "local"
pip install -r requirements.txt
python app.py
```

Después se accede a:

```text
http://localhost:5000/portal
```

## Pruebas

Desde la raíz del repositorio:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

## Despliegue en Azure

El despliegue real se realiza con PowerShell y Azure CLI:

```powershell
az login
$env:API_KEY = "<token-de-verificacion>"
.\scripts\deploy-azure.ps1
.\scripts\verify-azure.ps1
```

La Logic App se despliega con:

```powershell
$env:API_KEY = "<token-de-verificacion>"
.\scripts\deploy-logicapp.ps1
```

Los scripts configuran App Service, Cosmos DB Free Tier, Storage de apoyo, Key Vault, Managed Identity, variables de entorno y publicación del código. El token no se versiona en GitHub.

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Información básica del servicio. |
| `GET` | `/portal` | Portal web empresarial. |
| `GET` | `/ayuda` | Guía de uso integrada. |
| `GET` | `/acerca` | Versión, arquitectura y enlaces verificables. |
| `GET` | `/docs` | Documentación OpenAPI interactiva. |
| `GET` | `/openapi.json` | Contrato OpenAPI 3.0. |
| `GET` | `/health` | Estado técnico del sistema. |
| `GET` | `/catalogo` | Catálogo de servicios, activos y entornos. |
| `POST` | `/solicitudes` | Crear solicitud TI. |
| `GET` | `/solicitudes` | Listar solicitudes, protegido con Bearer token. |
| `GET/PATCH` | `/solicitudes/<id>` | Consultar y gestionar una solicitud. |
| `POST` | `/solicitudes/<id>/aprobacion` | Aprobar o rechazar una solicitud sensible. |
| `POST` | `/solicitudes/<id>/escalar` | Escalar una solicitud activa. |
| `POST` | `/solicitudes/<id>/valoracion` | Valorar una solicitud cerrada. |
| `GET` | `/metricas` | Métricas agregadas, protegido con Bearer token. |
| `GET` | `/operaciones` | Carga, alertas, SLA y satisfacción. |
| `GET` | `/informes/solicitudes.csv` | Exportación CSV protegida. |
| `POST` | `/demo/cargar` | Preparar escenario de demostración protegido. |

## Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| `src/` | API Flask, portal web, clasificador, almacenamiento y configuración. |
| `tests/` | Pruebas automáticas del comportamiento principal. |
| `scripts/` | Scripts de despliegue, migración Blob a Cosmos DB y verificación en Azure. |
| `logicapp/` | Definición del flujo de Logic App. |
| `infra/terraform/` | Infraestructura declarativa documentada en Terraform. |
| `infra/bicep/` | Plantillas Bicep de apoyo/documentación. |
| `memoria/` | Fuentes LaTeX, imágenes y PDF oficiales de memoria y anexos. |
| `docs/api/` | Documentación técnica de API y endpoints. |
| `docs/arquitectura/` | Evidencias y documentación de arquitectura Azure. |
| `docs/calidad/` | Evidencias de SonarCloud y calidad interna. |
| `docs/decisiones/` | Decisiones técnicas justificadas. |
| `docs/despliegue/` | Documentación de despliegue y verificación. |
| `docs/entrega/` | Base del PDF de enlaces y material de defensa. |
| `docs/evidencias/` | Capturas de Azure, portal, API, Logic App, Monitor, Zube, SonarCloud y GitHub. |
| `docs/sprints/` | Detalle de sprints, prioridades, puntos de historia y capturas de Zube. |

## Entregables

| Entregable | Ubicación |
|------------|-----------|
| Memoria | `memoria/memoria.pdf` |
| Anexos | `memoria/anexos.pdf` |
| Código fuente | `src/`, `logicapp/`, `infra/`, `scripts/` |
| Pruebas | `tests/` |
| Evidencias | `docs/evidencias/` |
| PDF de enlaces | Se genera a partir de `docs/entrega/enlaces-tfg.md` cuando estén publicados los dos vídeos. |
| Presentación de defensa | `docs/entrega/presentacion-defensa-tfg.pptx` |
| Cartel A3 | `docs/entrega/cartel-a3.pdf` |
| Release final | `v1.1.0` en GitHub Releases |
| Licencia | `LICENSE` |

## Vídeos obligatorios

La entrega requiere dos vídeos independientes, ambos de máximo cinco minutos:

1. Vídeo de presentación del TFG: introducción, objetivos, conceptos teóricos, técnicas y herramientas, trabajos relacionados y conclusiones.
2. Vídeo de demostración funcional: recorrido real por portal, solicitud, bandeja TI, aprobación, SLA, Logic App, Azure y SonarCloud.

El guion preparado para grabarlos está fuera del repositorio público de entrega, en la carpeta general del TFG.
