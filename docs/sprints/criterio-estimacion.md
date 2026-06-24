# Estimación relativa del backlog

Las historias de usuario se estiman con la escala Fibonacci `1, 2, 3, 5, 8 y 13`. La puntuación combina complejidad técnica, incertidumbre, dependencias y esfuerzo relativo; no representa horas de trabajo. Esta normalización permite comparar el tamaño de los incrementos y analizar las replanificaciones conservadas en Zube.

## Puntos por historia

| Sprint | Tarjeta | Historia | Puntos |
|--------|---------|----------|-------:|
| 1 | #1 | HU-01 Definir proceso empresarial | 3 |
| 1 | #2 | HU-02 Configurar Azure Students | 2 |
| 1 | #3 | HU-03 Estructurar repositorio y LaTeX | 3 |
| 1 | #4 | HU-04 Explorar CI/CD básico | 5 |
| 1 | #5 | HU-05 Diseñar arquitectura general | 5 |
| 1 | #6 | HU-06 Configurar seguimiento de calidad | 3 |
| 2 | #7 | HU-07 Crear Azure Key Vault | 3 |
| 2 | #8 | HU-08 Integrar Key Vault y App Service | 5 |
| 2 | #9 | HU-09 Crear API Python inicial | 5 |
| 2 | #10 | HU-10 Explorar GitHub Actions | 5 |
| 2 | #11 | HU-11 Crear sistema de incidencias | 8 |
| 2 | #12 | HU-12 Integrar clasificación | 5 |
| 3 | #13 | HU-13 Integrar almacenamiento persistente | 5 |
| 3 | #14 | HU-14 Consolidar Key Vault | 5 |
| 3 | #15 | HU-15 Implementar CI/CD completo | 8 |
| 3 | #16 | HU-16 Mejorar clasificación | 5 |
| 4 | #18 | HU-19 Integrar Terraform | 8 |
| 4 | #19 | HU-20 Documentar arquitectura cloud | 5 |
| 4 | #20 | HU-21 Completar memoria LaTeX | 8 |
| 4 | #21 | HU-22 Mejorar API empresarial | 8 |
| 4 | #22 | HU-23 Preparar evidencias técnicas | 5 |
| 5 | #23 | HU-24 Generar memoria final PDF | 8 |
| 5 | #24 | HU-25 Crear vídeo de demostración | 5 |
| 5 | #25 | HU-26 Crear vídeo de presentación | 5 |
| 5 | #26 | HU-27 Preparar defensa final | 5 |

## Resumen por sprint

| Sprint | Puntos comprometidos | Puntos completados en el sprint | Tratamiento |
|--------|---------------------:|--------------------------------:|-------------|
| Sprint 1 | 21 | 21 | Preparación, arquitectura y calidad inicial. |
| Sprint 2 | 31 | 31 | API, seguridad, incidencias y clasificación. |
| Sprint 3 | 23 | 5 | Se retiraron 18 puntos durante la replanificación. |
| Sprint 4 | 34 | 34 | Consolidación técnica y documental. |
| Sprint 5 | 23 | En curso | Cierre documental, vídeos y defensa. |

Los 18 puntos retirados del Sprint 3 corresponden a HU-13, HU-15 y HU-16. La persistencia y la clasificación se incorporaron posteriormente mediante Blob Storage y reglas deterministas; el pipeline completo se sustituyó por despliegue reproducible con PowerShell y Azure CLI. De esta forma, la diferencia entre puntos comprometidos y completados representa un cambio de alcance registrado, no trabajo oculto.

## Evidencias de seguimiento

La estimación relativa se interpreta junto con las fechas previstas y reales, las tarjetas cerradas, el historial de Zube, los commits, las releases y los incrementos funcionales. Las horas del Anexo A se reservan para la estimación económica y no se convierten directamente en puntos.

