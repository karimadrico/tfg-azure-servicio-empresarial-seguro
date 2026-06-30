# Sprint 6 - Mejora final de persistencia con Cosmos DB

Periodo previsto: 25/06/2026 - 30/06/2026.  
Cierre real previsto: 30/06/2026.  
Objetivo: reforzar la persistencia final del prototipo sustituyendo el uso principal de Blob Storage por Azure Cosmos DB, manteniendo el modelo documental JSON y dejando la solución más alineada con una arquitectura cloud empresarial.

## Tarjetas a registrar en Zube

| Tarjeta | Historia de usuario | Prioridad | Puntos | Labels recomendadas | Resultado esperado |
|---------|--------------------|:---------:|-------:|---------------------|--------------------|
| HU-28 | Crear Cosmos DB Free Tier | P1 | 3 | `azure`, `database`, `cosmosdb`, `security` | Cuenta `cosmos-tfg-kdr-2026`, base de datos `tfg-solicitudes`, contenedor `solicitudes` y partición `/tipo_solicitud`. |
| HU-29 | Implementar almacenamiento en Cosmos DB | P1 | 5 | `backend`, `api`, `cosmosdb`, `persistence` | Nueva clase de almacenamiento, configuración `STORAGE_MODE=cosmos` y eliminación de metadatos internos en respuestas API. |
| HU-30 | Migrar solicitudes desde Blob Storage | P1 | 2 | `migration`, `azure`, `data` | Migración de 20 solicitudes existentes conservando identificadores, historial y estructura JSON. |
| HU-31 | Verificar despliegue real con Cosmos DB | P1 | 2 | `testing`, `azure`, `validation` | `/health` devuelve `storage_mode: cosmos`, se crea `SOL-023`, la API lista 23 solicitudes y métricas responde correctamente. |
| HU-32 | Actualizar evidencias y documentación final | P2 | 1 | `documentation`, `evidence`, `latex`, `quality` | README, evidencias, diagramas, memoria/anexos y SonarCloud alineados con Cosmos DB. |

Total del Sprint 6: **13 puntos cerrados**.

## Criterio de planificación

Este sprint se añade como mejora final porque la revisión del diseño de datos detectó que un único blob JSON era suficiente para el prototipo inicial, pero menos adecuado para una solución empresarial con historial, aprobaciones, escalados, SLA y valoración. Cosmos DB permite conservar el enfoque documental del proyecto y representar cada solicitud como un documento independiente.

El alcance se mantiene acotado: no se rediseña toda la aplicación ni se incorpora una base de datos relacional. Se sustituye la persistencia principal por Cosmos DB, se migra la información existente, se valida el despliegue y se actualiza la documentación para que el producto entregado y la memoria describan la misma solución.
