# Diagramas del sistema

Este documento recoge los diagramas que deben acompañar a la memoria y a los anexos del TFG. Los diagramas finales deben ser de elaboración propia y guardarse como PNG en `memoria/img/`, porque esa carpeta es la que se usa desde LaTeX para generar `memoria.pdf` y `anexos.pdf`.

La recomendación es crearlos con diagrams.net/draw.io o con una herramienta de generación visual y revisarlos manualmente antes de incorporarlos al documento. No deben mostrar secretos, tokens, cadenas de conexión ni URLs de Logic App con firma `sig`.

## Diagramas finales a crear

| Archivo final | Donde se usara | Contenido esperado |
|----------------|----------------|--------------------|
| `arquitectura_final_azure.png` | Memoria y Anexo C | Vista completa de la solución: usuario, portal, App Service, API Flask, clasificador ligero, Blob Storage, Key Vault, Managed Identity, Application Insights, Logic App, GitHub, Zube y SonarCloud. |
| `flujo_solicitud_ti.png` | Anexo C y Manual de usuario | Flujo funcional: usuario o Logic App envia solicitud, API valida, clasificador calcula prioridad/categoria, Storage persiste, API devuelve `SOL-XXX`. |
| `despliegue_azure.png` | Anexo D | Flujo de despliegue: repositorio GitHub, scripts PowerShell, Azure CLI, App Service, Key Vault, Storage, Application Insights y script de verificacion. |
| `seguridad_secretos.png` | Memoria y Anexo C | Modelo de seguridad: Key Vault almacena `api-key`, App Service usa Managed Identity, endpoints protegidos con Bearer token, HTTPS y variables de entorno. |
| `calidad_planificacion.png` | Anexo A y Anexo D | Relación entre Zube, commits GitHub, SonarCloud, pruebas automáticas y evidencias de despliegue. |
| `logic_app_workflow.png` | Anexo C o D | Orquestación de Logic App: trigger HTTP, acción HTTP `POST /solicitudes`, respuesta al cliente y almacenamiento final vía API. |
| `observabilidad_monitor.png` | Anexo D | Monitorización: App Service emite métricas/logs, Application Insights recoge telemetría y Azure Monitor permite revisar disponibilidad y errores. |

## Criterios de elaboración de diagramas

Los diagramas finales se elaboran como documentación técnica propia del proyecto. Deben mantener un estilo homogéneo, utilizar nombres de servicios reales del despliegue y evitar cualquier dato sensible. Para su incorporación a LaTeX se exportan en formato PNG horizontal y alta resolución.

Criterios comunes:

- Usar fondo claro y etiquetas en español.
- Agrupar los recursos cloud dentro de un bloque "Microsoft Azure".
- Separar los servicios de soporte al proceso, como GitHub, Zube y SonarCloud.
- Representar únicamente recursos desplegados, verificados o documentados como parte del prototipo.
- No incluir tokens, claves, cadenas de conexión ni URL de Logic App con firma.
## Diagrama de componentes

```mermaid
flowchart TB
    usuario[Usuario / Tribunal] --> portal[Portal web en App Service]
    portal --> api[API Flask]
    api --> clasificador[Clasificador ligero]
    api --> storage[Azure Blob Storage]
    api --> keyvault[Azure Key Vault]
    api --> appinsights[Application Insights]
    logicapp[Logic App HTTP] --> api
    appid[Managed Identity] --> keyvault
    api --> health[Endpoint /health]
    api --> metricas[Endpoint /metricas]
```

## Flujo de creación de solicitud

```mermaid
sequenceDiagram
    actor Usuario
    participant Portal
    participant API
    participant Clasificador
    participant Storage

    Usuario->>Portal: Rellena solicitud TI
    Portal->>API: POST /solicitudes
    API->>API: Valida campos obligatorios
    API->>Clasificador: Calcula tipo, prioridad y recomendación
    Clasificador-->>API: Resultado de clasificación
    API->>Storage: Guarda documento JSON
    Storage-->>API: Confirmación
    API-->>Portal: Respuesta con identificador SOL-XXX
```

## Flujo de Logic App

```mermaid
sequenceDiagram
    actor SistemaExterno
    participant LogicApp
    participant API
    participant Clasificador
    participant Storage

    SistemaExterno->>LogicApp: POST HTTP con solicitud TI
    LogicApp->>API: POST /solicitudes con Bearer token
    API->>API: Valida JSON recibido
    API->>Clasificador: Clasifica tipo, prioridad y categoria
    API->>Storage: Persiste solicitud
    API-->>LogicApp: 201 Created con SOL-XXX
    LogicApp-->>SistemaExterno: Respuesta de la API
```

## Despliegue y verificación

```mermaid
flowchart LR
    repo[Repositorio GitHub] --> script[deploy-azure.ps1]
    script --> azcli[Azure CLI]
    azcli --> app[Azure App Service]
    azcli --> kv[Azure Key Vault]
    azcli --> blob[Azure Blob Storage]
    azcli --> ai[Application Insights]
    logic[deploy-logicapp.ps1] --> la[Azure Logic App]
    verify[verify-azure.ps1] --> app
    verify --> endpoints[/, /health, /solicitudes, /metricas]
```

## Relación entre evidencias

```mermaid
flowchart TB
    zube[Zube: sprints y tareas] --> repo[Commits GitHub]
    repo --> sonar[SonarCloud: calidad]
    repo --> azure[Despliegue Azure]
    azure --> portal[Portal funcional]
    azure --> api[API REST]
    repo --> memoria[Memoria y anexos PDF]
```

