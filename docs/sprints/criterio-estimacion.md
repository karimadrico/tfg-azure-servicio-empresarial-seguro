# Criterio de estimación y seguimiento

## Decisión aplicada

Las historias se planificaron y siguieron mediante tarjetas, fechas previstas, fechas reales y estado de cierre. No se asignaron puntos de historia antes de comenzar los sprints. Por este motivo, Zube muestra cero puntos aunque las tarjetas estén cerradas y no puede generar un burndown de puntos representativo.

No se deben asignar puntos de forma retroactiva a los sprints cerrados: el gráfico resultante aparentaría una estimación que no existió durante el desarrollo. La ausencia de puntos se conserva como una limitación del proceso y como aprendizaje para una siguiente iteración.

## Evidencias utilizadas

El seguimiento puede comprobarse mediante:

- fechas previstas y reales de cada sprint;
- tarjetas cerradas y cambios de alcance registrados en Zube;
- commits asociados a cada incremento;
- versiones y releases funcionales;
- capturas de Azure, pruebas y documentación generada.

Las horas por fase del Anexo A se usan para el cálculo económico, no como sustituto de los puntos de historia.

## Respuesta preparada para la defensa

> No asigné story points durante la planificación inicial, así que no sería correcto reconstruir ahora un burndown retrospectivo. Utilicé tarjetas, fechas, commits e incrementos funcionales como evidencias de avance. Es una limitación de mi aplicación del marco ágil: en un siguiente proyecto realizaría una sesión de estimación antes de cada sprint, mantendría una escala estable y revisaría la velocidad al terminar cada iteración.

## Cómo utilizar puntos en una iteración futura

1. Revisar el backlog antes de iniciar el sprint.
2. Asignar a cada historia una estimación relativa con escala Fibonacci: 1, 2, 3, 5, 8 y 13.
3. Valorar conjuntamente complejidad, incertidumbre, esfuerzo y dependencias; no convertir horas directamente en puntos.
4. Dividir una historia si supera 13 puntos.
5. Iniciar el sprint cuando todas sus historias estén estimadas.
6. No modificar los puntos una vez iniciado; si cambia el alcance, registrar la replanificación.
7. Comparar puntos comprometidos y terminados para obtener velocidad y burndown reales.

## Cierre del Sprint 5

El Sprint 5 debe cerrarse en Zube cuando sus cuatro tarjetas estén realmente terminadas:

1. Finalizar y cerrar HU-24, HU-25, HU-26 y HU-27.
2. Abrir el Sprint Board del Sprint 5.
3. Comprobar que no quedan tarjetas en progreso.
4. Pulsar `Close` y conservar la fecha real de cierre.
5. Guardar una captura del sprint cerrado en `docs/sprints/`.
6. Actualizar `resumen-sprints.md`, `zube-detalle.md` y la tabla A.2 de los anexos.

