# Seguimiento detallado en Zube

Tablero principal: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban

Este documento conserva la planificación real observada en Zube. Las fechas de cierre posteriores al final previsto reflejan desviaciones del calendario y las tarjetas retiradas representan decisiones de replanificación, no eliminación del trabajo realizado.

## Sprint 1 - Preparación y base

- Periodo previsto: 25/02/2026 - 10/03/2026.
- Cierre real: 15/03/2026.
- Objetivo: definir el proceso empresarial, estructurar el repositorio, preparar Azure, planificar la arquitectura y configurar el seguimiento inicial de calidad.
- Resultado Zube: 6 tarjetas cerradas de 6; no se utilizaron puntos de historia.
- Vista de tarjetas cerradas: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/manager?where%5Bproject_id%5D=33139&where%5Bworkspace_id%5D=38369&where%5Bsprint_ids%5D%5B%5D=62216

| Tarjeta | Historia de usuario | Resultado |
|---------|--------------------|-----------|
| [#1](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/1) | HU-01 Definir proceso empresarial a automatizar | Cerrada el 15/03/2026 |
| [#2](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/2) | HU-02 Configurar cuenta de Azure Students | Cerrada el 15/03/2026 |
| [#3](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/3) | HU-03 Estructurar repositorio y plantillas LaTeX | Cerrada el 15/03/2026 |
| [#4](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/4) | HU-04 Configurar CI/CD básico | Cerrada como exploración inicial; el mecanismo final cambió a PowerShell y Azure CLI |
| [#5](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/5) | HU-05 Diseñar arquitectura general | Cerrada el 15/03/2026 |
| [#6](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/6) | HU-06 Configurar gestor de calidad | Cerrada; la solución final utiliza SonarCloud |

## Sprint 2 - Implementación de módulos y dashboard

- Periodo previsto: 11/03/2026 - 24/03/2026.
- Cierre real: 17/04/2026.
- Objetivo: desarrollar API, gestión de incidencias, seguridad inicial, clasificación ligera y primeras pruebas.
- Resultado Zube: 6 tarjetas cerradas de 6; no se utilizaron puntos de historia.
- Vista de tarjetas cerradas: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/manager?where%5Bproject_id%5D=33139&where%5Bworkspace_id%5D=38369&where%5Bsprint_ids%5D%5B%5D=62217

| Tarjeta | Historia de usuario | Resultado |
|---------|--------------------|-----------|
| [#7](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/7) | HU-07 Crear Azure Key Vault | Cerrada el 16/03/2026 |
| [#8](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/8) | HU-08 Integrar Key Vault con App Service | Cerrada el 16/03/2026 |
| [#9](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/9) | HU-09 Crear API Python inicial | Cerrada el 17/04/2026 |
| [#10](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/10) | HU-10 Configurar CI/CD con GitHub Actions | Cerrada como prueba inicial; no forma parte del despliegue final |
| [#11](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/11) | HU-11 Crear sistema de incidencias | Cerrada el 17/04/2026 |
| [#12](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/12) | HU-12 Integrar clasificación de incidencias | Cerrada el 17/04/2026 |

## Sprint 3 - Incidencias y despliegue

- Periodo previsto: 25/03/2026 - 21/04/2026.
- Cierre real: 20/05/2026.
- Objetivo: consolidar seguridad, persistencia, clasificación y despliegue del prototipo.
- Resultado Zube: una tarjeta permaneció asignada y cerrada; tres tarjetas fueron retiradas del sprint durante la replanificación.
- Vista del sprint: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/manager?where%5Bproject_id%5D=33139&where%5Bworkspace_id%5D=38369&where%5Bsprint_ids%5D%5B%5D=62218

| Tarjeta | Cambio registrado | Tratamiento final |
|---------|-------------------|-------------------|
| [#14](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/14) | HU-14 Integrar Azure Key Vault correctamente | Cerrada el 30/04/2026 dentro del Sprint 3 |
| [#13](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/13) | HU-13 Integrar almacenamiento persistente; retirada el 17/04/2026 | Replanificada y materializada mediante Azure Blob Storage |
| [#15](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/15) | HU-15 Implementar CI/CD completo; retirada el 17/04/2026 | Descartada del alcance final; se adoptó despliegue reproducible con PowerShell y Azure CLI |
| [#16](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/16) | HU-16 Mejorar clasificación; retirada el 17/04/2026 | Replanificada y completada como clasificador determinista con reglas y pruebas |

## Sprint 4 - Consolidación y documentación técnica

- Periodo previsto: 22/04/2026 - 21/05/2026.
- Cierre real: 22/05/2026.
- Objetivo: consolidar arquitectura, infraestructura como código, API, memoria, anexos y evidencias.
- Resultado Zube: 5 tarjetas cerradas de 5.
- Vista de tarjetas cerradas: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/manager?where%5Bproject_id%5D=33139&where%5Bworkspace_id%5D=38369&where%5Bsprint_ids%5D%5B%5D=62577

| Tarjeta | Historia de usuario | Resultado |
|---------|--------------------|-----------|
| [#18](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/18) | HU-19 Integrar Terraform | Cerrada el 22/05/2026 |
| [#19](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/19) | HU-20 Documentar arquitectura cloud | Cerrada el 22/05/2026 |
| [#20](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/20) | HU-21 Completar memoria LaTeX | Cerrada el 22/05/2026 |
| [#21](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/21) | HU-22 Mejorar API empresarial | Cerrada el 22/05/2026 |
| [#22](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/22) | HU-23 Preparar evidencias técnicas | Cerrada el 22/05/2026 |

## Sprint 5 - Finalización y defensa

- Periodo: 22/05/2026 - 08/07/2026.
- Estado: abierto.
- Objetivo: cerrar documentación, vídeos, validación, defensa y entrega oficial.
- Resultado actual: 4 tarjetas en progreso.
- Tablero del sprint: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/sprintboard?where%5Bsprint_id%5D=62587

| Tarjeta | Historia de usuario | Estado |
|---------|--------------------|--------|
| [#23](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/23) | HU-24 Generar memoria final PDF | En progreso |
| [#24](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/24) | HU-25 Crear vídeo de demostración | En progreso |
| [#25](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/25) | HU-26 Crear vídeo de presentación | En progreso |
| [#26](https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/c/26) | HU-27 Preparar defensa final | En progreso |

## Interpretación de puntos y tarjetas

Zube muestra cero puntos porque no se utilizaron puntos de historia como unidad de estimación. La estimación y el coste se documentan mediante horas por fase en el Anexo A. Las tarjetas cerradas reflejan finalización de tareas; los cambios de alcance se conservan de forma explícita para no alterar retrospectivamente el historial del proyecto.
