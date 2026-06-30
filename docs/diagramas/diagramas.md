# Diagramas del sistema

La documentación visual del proyecto combina imágenes exportadas a `memoria/img/` y diagramas nativos en LaTeX. Los diagramas se han revisado para que coincidan con la arquitectura final: App Service, API Flask, Cosmos DB, Key Vault, Managed Identity, Logic App, Application Insights, Zube, GitHub y SonarCloud.

## Inventario

| Diagrama | Documento | Contenido |
|----------|-----------|-----------|
| `arquitectura_integral_tfg_azure.png` | README y memoria | Vista global de producto, Azure y evidencias de proceso. |
| `arquitectura_final_azure.png` | Memoria y Anexo C | Arquitectura cloud centrada en App Service, API, Cosmos DB, Key Vault, Logic App y Monitor. |
| `flujo_solicitud_ti.png` | Anexo C | Validación, clasificación, cálculo de impacto, persistencia y respuesta `SOL-XXX`. |
| `despliegue_azure.png` | Anexo D | Repositorio, PowerShell, Azure CLI, recursos de Azure y verificación. |
| `seguridad_secretos.png` | Memoria y Anexo C | Token en Key Vault, Managed Identity, HTTPS y endpoints protegidos. |
| `calidad_planificacion.png` | Anexos A y D | Relación entre Zube, GitHub, pruebas, SonarCloud y despliegue. |
| `logic_app_workflow.png` | Anexos C y D | Trigger HTTP, llamada a `POST /solicitudes` y respuesta al sistema externo. |
| `observabilidad_monitor.png` | Anexo D | Telemetría de App Service, Application Insights y Azure Monitor. |

Los modelos de casos de uso, entidades, estados y secuencias se generan directamente con TikZ en los anexos B y C. Todos los diagramas omiten tokens, cadenas de conexión y URLs firmadas.

## Diagrama de componentes

```mermaid
flowchart TB
    usuario[Usuario / Tribunal] --> portal[Portal web en App Service]
    sistema[Sistema externo HTTP] --> logicapp[Logic App]
    logicapp --> api[API Flask]
    portal --> api
    api --> reglas[Reglas de negocio]
    reglas --> cosmos[Azure Cosmos DB]
    api --> keyvault[Azure Key Vault]
    appid[Managed Identity] --> keyvault
    api --> appinsights[Application Insights]
    api --> health[Endpoint health]
    api --> metricas[Endpoint metricas]
```

## Flujo de creación de solicitud

```mermaid
sequenceDiagram
    actor Usuario
    participant Portal
    participant API
    participant Reglas
    participant Cosmos

    Usuario->>Portal: Rellena solicitud TI
    Portal->>API: POST /solicitudes
    API->>API: Valida campos y catálogo
    API->>Reglas: Calcula prioridad, impacto y SLA
    Reglas-->>API: Resultado de clasificación
    API->>Cosmos: Guarda documento JSON
    Cosmos-->>API: Confirmación
    API-->>Portal: Respuesta con identificador SOL-XXX
```

## Flujo de Logic App

```mermaid
sequenceDiagram
    actor SistemaExterno
    participant LogicApp
    participant API
    participant Reglas
    participant Cosmos

    SistemaExterno->>LogicApp: POST HTTP con solicitud TI
    LogicApp->>API: POST /solicitudes con Bearer token
    API->>API: Valida JSON recibido
    API->>Reglas: Clasifica tipo, prioridad e impacto
    API->>Cosmos: Persiste solicitud
    API-->>LogicApp: 201 Created con SOL-XXX
    LogicApp-->>SistemaExterno: Respuesta de la API
```

## Despliegue y verificación

```mermaid
flowchart LR
    repo[Repositorio GitHub] --> deploy[deploy-azure.ps1]
    deploy --> azcli[Azure CLI]
    azcli --> app[Azure App Service]
    azcli --> kv[Azure Key Vault]
    azcli --> cosmos[Azure Cosmos DB]
    azcli --> ai[Application Insights]
    logicdeploy[deploy-logicapp.ps1] --> logic[Azure Logic App]
    verify[verify-azure.ps1] --> app
    verify --> endpoints[health solicitudes metricas portal]
```

## Relación entre evidencias

```mermaid
flowchart TB
    zube[Zube: sprints y tareas] --> repo[Commits GitHub]
    repo --> sonar[SonarCloud: calidad]
    repo --> azure[Despliegue Azure]
    azure --> portal[Portal funcional]
    azure --> api[API REST]
    azure --> cosmos[Cosmos DB]
    repo --> memoria[Memoria y anexos PDF]
```
