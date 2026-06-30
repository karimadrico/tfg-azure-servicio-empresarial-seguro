# Resumen de sprints en Zube

Tablero: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban

| Sprint | Fechas | Estado | Puntos | Objetivo |
|--------|--------|--------|-------:|----------|
| Sprint 1 - Preparación y base | 25/02/2026 - 10/03/2026 | Cerrado 15/03/2026 | 21 | Definir proceso, repositorio, Azure inicial, validación inicial y arquitectura base. |
| Sprint 2 - Implementación de módulos y dashboard | 11/03/2026 - 24/03/2026 | Cerrado 17/04/2026 | 31 | Desarrollar módulos, dashboard, clasificación por reglas y primeras pruebas unitarias. |
| Sprint 3 - Incidencias y despliegue | 25/03/2026 - 21/04/2026 | Cerrado 20/05/2026 | 23 | Integrar incidencias, seguridad, pruebas finales y despliegue Azure. |
| Sprint 4 - Consolidación y documentación técnica | 22/04/2026 - 21/05/2026 | Cerrado 22/05/2026 | 34 | Consolidar arquitectura cloud, API, documentación técnica, anexos y evidencias. |
| Sprint 5 - Finalización y defensa | 22/05/2026 - 24/06/2026 | Cerrado 24/06/2026 | 23 | Cerrar memoria/anexos, calidad, validación final y preparar defensa y entregables. |
| Sprint 6 - Mejora final de persistencia con Cosmos DB | 25/06/2026 - 30/06/2026 | Cerrado 30/06/2026 | 13 | Sustituir la persistencia principal por Cosmos DB, migrar datos y cerrar evidencias finales. |

## Evidencias

Las capturas de Zube se conservan en `docs/sprints/` y permiten comprobar la evolución incremental del proyecto. Los sprints cerrados muestran la evolución incremental del proyecto. El Sprint 5 cerró la entrega documental el 24 de junio y el Sprint 6 recoge la mejora final de persistencia con Cosmos DB cerrada el 30 de junio.

![Resumen final de los cinco sprints en Zube](sprints-finalizacion-storypoints.png)

Con esta mejora, el backlog completo suma 145 puntos estimados: 127 puntos cerrados en sprints y 18 puntos retirados del Sprint 3 durante la replanificación. Las capturas `sprint1-final.png`, `sprint2-final.png`, `sprint3-final.png`, `sprint3-final-retiradas.png`, `sprint4-final.png`, `sprint5-final.png` y la captura final del Sprint 6 permiten revisar cada iteración por separado.

El inventario de tarjetas, enlaces y decisiones de replanificación se encuentra en [`zube-detalle.md`](zube-detalle.md).

## Estimación relativa

El backlog utiliza una escala Fibonacci para comparar complejidad, incertidumbre y dependencias. En el Sprint 3 se comprometieron 23 puntos: 5 se cerraron dentro de la iteración y 18 se retiraron durante la replanificación. La asignación por historia y el tratamiento de esos cambios se detallan en [`criterio-estimacion.md`](criterio-estimacion.md).

Los dos primeros sprints fueron más cortos porque cubrían la preparación del entorno, el diseño inicial y la primera versión del prototipo. Los sprints posteriores concentraron despliegue cloud, validación, documentación académica y cierre de evidencias, por lo que se ampliaron hasta completar incrementos verificables. Algunas historias aparecen cerradas el mismo día porque la revisión de sprint se registró de forma agrupada después de comprobar código, capturas y documentación asociada.
