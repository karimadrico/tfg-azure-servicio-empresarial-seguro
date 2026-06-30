# Infraestructura cloud en Azure

La infraestructura final se despliega en Microsoft Azure con un enfoque de servicios gestionados. El despliegue operativo se realiza mediante scripts PowerShell y Azure CLI, mientras que las carpetas `infra/bicep/` e `infra/terraform/` documentan la forma declarativa de los recursos.

## Componentes principales

| Componente | Función |
|------------|---------|
| Resource Group `rg-tfg-cloudautomation-dev` | Agrupa los recursos del TFG en una unidad de gestión. |
| App Service `app-tfg-incidencias-dev` | Ejecuta la API Flask y sirve el portal web. |
| Azure Cosmos DB `cosmos-tfg-kdr-2026` | Persiste las solicitudes como documentos JSON independientes. |
| Key Vault `kv-tfg-incidencias-dev` | Conserva el secreto `api-key` fuera del repositorio. |
| Managed Identity | Permite al App Service acceder a Key Vault sin credenciales embebidas. |
| Logic App `logic-tfg-solicitudes-dev` | Recibe solicitudes HTTP desde sistemas externos y llama a la API. |
| Application Insights `appi-tfg-incidencias-dev` | Recoge telemetría básica y apoya la observabilidad. |
| Storage Account `sttfgincidenciasdev` | Conserva la persistencia inicial y sirve como origen de migración. |

## Persistencia final

La persistencia principal es Cosmos DB. La base de datos `tfg-solicitudes` contiene el contenedor `solicitudes`, particionado por `/tipo_solicitud`. La aplicación se ejecuta con `STORAGE_MODE=cosmos`; el modo local y el modo Blob se mantienen como apoyo de desarrollo y compatibilidad, pero no describen la arquitectura final desplegada.

## Verificación

La verificación del despliegue se realiza con `scripts/verify-azure.ps1`. El recorrido comprueba que `/health` responde con `storage_mode: cosmos`, que se puede crear una solicitud, listar solicitudes protegidas y consultar métricas. Las evidencias visuales se conservan en `docs/evidencias/`.
