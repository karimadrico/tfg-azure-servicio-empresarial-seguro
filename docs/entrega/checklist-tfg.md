# Checklist de entrega TFG

## Entregables obligatorios

| Requisito | Estado | Evidencia |
|-----------|--------|-----------|
| Memoria PDF | Preparado | `memoria/memoria.pdf` |
| Anexos PDF | Preparado | `memoria/anexos.pdf` |
| Código fuente | Preparado | `src/`, `tests/`, `infra/`, `logicapp/` |
| Repositorio GitHub | Preparado | `README.md` |
| Gestión de tareas en iteraciones | Preparado | Zube y capturas en `docs/sprints/` |
| Despliegue cloud | Preparado | Azure App Service y guías en `docs/despliegue/` |
| Calidad de código | En ejecución | SonarCloud configurado en `.github/workflows/sonarcloud.yml` |
| Vídeo de presentación | Pendiente de enlace final | Debe durar máximo 5 minutos |
| Vídeo de demostración | Pendiente de enlace final | Debe durar máximo 5 minutos |
| PDF con enlaces de entrega | Pendiente | Debe incluir vídeos, repositorio, despliegue y SonarCloud |

## Reglas revisadas

| Criterio | Estado | Comentario |
|----------|--------|------------|
| Mínimo tres sprints | Cumplido | Se documentan cinco iteraciones. |
| Uso de gestor de tareas | Cumplido | Zube se referencia en README y anexos. |
| Requisitos funcionales y no funcionales | Cumplido | Anexo B. |
| Casos de uso | Cumplido básico | Tabla de casos de uso en Anexo B. |
| Diseño de datos | Cumplido básico | Diccionario de datos documental en Anexo C. |
| Pruebas automáticas | Cumplido | `tests/test_api.py`. |
| Despliegue en nube | Cumplido | Azure App Service. |
| Licencias | Cumplido básico | Tabla de licencias en Anexo A y `LICENSE`. |
| Costes con cargas empresariales | Cumplido básico | Anexo A. |
| Sostenibilidad 600-800 palabras | Cumplido | Anexo F. |
| Bibliografía citada en texto | Cumplido | Memoria y anexos incluyen citas. |
| Calidad con SonarQube/SonarCloud | En curso | Falta confirmar ejecución correcta y guardar evidencia. |
| Tres releases | Recomendable | Crear al menos `v1.0.0` final; idealmente tres tags/releases. |

## Acciones pendientes antes de entregar

1. Ejecutar GitHub Actions y confirmar que SonarCloud finaliza correctamente.
2. Guardar captura del Quality Gate de SonarCloud.
3. Comprobar en Azure que `/portal`, `/health`, creación de solicitudes y consulta de métricas responden.
4. Grabar vídeo de presentación con cámara y audio.
5. Grabar vídeo de demostración funcional con el portal, API, Azure Portal y Logic App.
6. Crear el PDF de enlaces finales para UBUVirtual.
7. Crear release final en GitHub, por ejemplo `v1.0.0`.
