# Diagramas del sistema

Este documento recoge diagramas textuales en Mermaid para complementar las capturas y la arquitectura incluida en la memoria y los anexos. Los diagramas son de elaboración propia y reflejan el alcance final entregado: Azure App Service, Flask, Blob Storage, Key Vault, Managed Identity, Zube, SonarCloud y scripts PowerShell.

## Diagrama de componentes

```mermaid
flowchart TB
    usuario[Usuario / Tribunal] --> portal[Portal web en App Service]
    portal --> api[API Flask]
    api --> clasificador[Clasificador ligero]
    api --> storage[Azure Blob Storage]
    api --> keyvault[Azure Key Vault]
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

## Despliegue y verificación

```mermaid
flowchart LR
    repo[Repositorio GitHub] --> script[deploy-azure.ps1]
    script --> azcli[Azure CLI]
    azcli --> app[Azure App Service]
    azcli --> kv[Azure Key Vault]
    azcli --> blob[Azure Blob Storage]
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
