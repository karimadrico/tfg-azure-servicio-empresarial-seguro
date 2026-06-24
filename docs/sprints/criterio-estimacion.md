# Estimación relativa del backlog

Las historias de usuario se estiman con la escala Fibonacci `1, 2, 3, 5, 8 y 13`. La puntuación combina complejidad técnica, incertidumbre, dependencias y esfuerzo relativo; no representa horas de trabajo. La prioridad utiliza la escala de Zube, donde P1 identifica el trabajo imprescindible y P5 el de menor urgencia. Esta normalización permite comparar el tamaño de los incrementos y analizar las replanificaciones conservadas en Zube.

## Sprint 1 - Preparación y base

| Tarjeta | Historia | Prioridad | Puntos | Estado |
|---------|----------|:---------:|-------:|--------|
| #1 | HU-01 Definir proceso empresarial | P1 | 3 | Cerrada |
| #2 | HU-02 Configurar Azure Students | P1 | 2 | Cerrada |
| #3 | HU-03 Estructurar repositorio y LaTeX | P2 | 3 | Cerrada |
| #4 | HU-04 Explorar CI/CD básico | P3 | 5 | Cerrada |
| #5 | HU-05 Diseñar arquitectura general | P1 | 5 | Cerrada |
| #6 | HU-06 Configurar seguimiento de calidad | P2 | 3 | Cerrada |

Total del Sprint 1: **21 puntos cerrados**.

## Sprint 2 - Implementación de módulos y dashboard

| Tarjeta | Historia | Prioridad | Puntos | Estado |
|---------|----------|:---------:|-------:|--------|
| #7 | HU-07 Crear Azure Key Vault | P1 | 3 | Cerrada |
| #8 | HU-08 Integrar Key Vault y App Service | P1 | 5 | Cerrada |
| #9 | HU-09 Crear API Python inicial | P1 | 5 | Cerrada |
| #10 | HU-10 Explorar GitHub Actions | P3 | 5 | Cerrada |
| #11 | HU-11 Crear sistema de incidencias | P1 | 8 | Cerrada |
| #12 | HU-12 Integrar clasificación | P2 | 5 | Cerrada |

Total del Sprint 2: **31 puntos cerrados**.

## Sprint 3 - Incidencias y despliegue

| Tarjeta | Historia | Prioridad | Puntos | Estado |
|---------|----------|:---------:|-------:|--------|
| #13 | HU-13 Integrar almacenamiento persistente | P1 | 5 | Retirada y replanificada |
| #14 | HU-14 Consolidar Key Vault | P1 | 5 | Cerrada |
| #15 | HU-15 Implementar CI/CD completo | P3 | 8 | Retirada |
| #16 | HU-16 Mejorar clasificación | P2 | 5 | Retirada y replanificada |

Total del Sprint 3: **23 puntos comprometidos, 5 cerrados y 18 retirados**.

## Sprint 4 - Consolidación y documentación técnica

| Tarjeta | Historia | Prioridad | Puntos | Estado |
|---------|----------|:---------:|-------:|--------|
| #18 | HU-19 Integrar Terraform | P3 | 8 | Cerrada |
| #19 | HU-20 Documentar arquitectura cloud | P2 | 5 | Cerrada |
| #20 | HU-21 Completar memoria LaTeX | P1 | 8 | Cerrada |
| #21 | HU-22 Mejorar API empresarial | P1 | 8 | Cerrada |
| #22 | HU-23 Preparar evidencias técnicas | P2 | 5 | Cerrada |

Total del Sprint 4: **34 puntos cerrados**.

## Sprint 5 - Finalización y defensa

| Tarjeta | Historia | Prioridad | Puntos | Estado |
|---------|----------|:---------:|-------:|--------|
| #23 | HU-24 Generar memoria final PDF | P1 | 8 | Cerrada |
| #24 | HU-25 Crear vídeo de demostración | P1 | 5 | Cerrada |
| #25 | HU-26 Crear vídeo de presentación | P1 | 5 | Cerrada |
| #26 | HU-27 Preparar defensa final | P1 | 5 | Cerrada |

Total del Sprint 5: **23 puntos cerrados**.

## Resumen por sprint

| Sprint | Puntos comprometidos | Puntos completados en el sprint | Tratamiento |
|--------|---------------------:|--------------------------------:|-------------|
| Sprint 1 | 21 | 21 | Preparación, arquitectura y calidad inicial. |
| Sprint 2 | 31 | 31 | API, seguridad, incidencias y clasificación. |
| Sprint 3 | 23 | 5 | Se retiraron 18 puntos durante la replanificación. |
| Sprint 4 | 34 | 34 | Consolidación técnica y documental. |
| Sprint 5 | 23 | 23 | Cierre documental, validación y preparación de la defensa. |

El backlog estimado suma 132 puntos. Zube registra 114 puntos cerrados dentro de los sprints y 18 puntos retirados del Sprint 3, correspondientes a HU-13, HU-15 y HU-16. La persistencia y la clasificación se incorporaron posteriormente mediante Blob Storage y reglas deterministas; el pipeline completo se sustituyó por despliegue reproducible con PowerShell y Azure CLI. De esta forma, la diferencia representa un cambio de alcance registrado, no trabajo oculto.

## Evidencias de seguimiento

La estimación relativa se interpreta junto con las fechas previstas y reales, las tarjetas cerradas, el historial de Zube, los commits, las releases y los incrementos funcionales. Las horas del Anexo A se reservan para la estimación económica y no se convierten directamente en puntos.
