# v1.2.0 - Versión final con Cosmos DB y Sprint 6

Versión final del TFG tras incorporar la persistencia documental en Azure Cosmos DB y cerrar el Sprint 6 de mejora final.

## Cambios principales

- Persistencia final en Azure Cosmos DB.
- Cuenta Cosmos DB: `cosmos-tfg-kdr-2026`.
- Base de datos: `tfg-solicitudes`.
- Contenedor: `solicitudes`.
- Clave de partición: `/tipo_solicitud`.
- Migración de 20 solicitudes existentes desde Blob Storage.
- App Service configurado con `STORAGE_MODE=cosmos`.
- Verificación real en Azure con `/health`, creación de solicitud, listado y métricas.
- Corrección para no devolver metadatos internos de Cosmos DB en la API.
- Sprint 6 cerrado en Zube: 13 puntos y 5 tarjetas completadas.
- README, memoria, anexos, diagramas, evidencias y presentación actualizados.
- SonarCloud final documentado con Quality Gate aprobado.
- 27 pruebas automáticas superadas.

## Entregables incluidos

- `memoria/memoria.pdf`
- `memoria/anexos.pdf`
- `docs/entrega/presentacion-defensa-tfg.pptx`
- Código fuente de API, portal, Logic App, scripts e infraestructura.
- Evidencias de Azure, Cosmos DB, Zube, SonarCloud y portal en `docs/evidencias/` y `docs/sprints/`.
