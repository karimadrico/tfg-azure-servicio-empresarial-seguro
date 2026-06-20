# Checklist de entrega TFG

## Entregables obligatorios

| Requisito | Estado | Evidencia |
|-----------|--------|-----------|
| Memoria PDF | Preparado | `memoria/memoria.pdf` |
| Anexos PDF | Preparado | `memoria/anexos.pdf` |
| Código fuente | Preparado | `src/`, `tests/`, `scripts/`, `infra/` |
| Repositorio GitHub | Preparado | `README.md` y enlace público/compartido |
| Gestión de tareas | Preparado | Zube y capturas en `docs/sprints/` |
| Despliegue cloud | Preparado | Azure App Service y guías en `docs/despliegue/` |
| Calidad de código | Preparado | SonarCloud manual: `docs/calidad/sonarcloud.md` |
| Vídeo de presentación | Pendiente | Máximo 5 minutos, cámara y audio |
| Vídeo de demostración | Pendiente | Máximo 5 minutos, producto funcionando |
| PDF con enlaces | Pendiente | Falta sustituir URLs de vídeos en `docs/entrega/enlaces-tfg.md` y exportar a PDF |

## Reglas revisadas

| Criterio | Estado | Comentario |
|----------|--------|------------|
| Mínimo tres sprints | Cumplido | Se documentan cinco iteraciones. |
| Uso de gestor de tareas | Cumplido | Zube se referencia en README y anexos. |
| Requisitos funcionales y no funcionales | Cumplido | Anexo B. |
| Casos de uso | Cumplido | Tabla de casos de uso en Anexo B. |
| Diseño de datos | Cumplido | Diccionario documental en Anexo C. |
| Pruebas automáticas | Cumplido | `tests/test_api.py`. |
| Despliegue en nube | Cumplido | Azure App Service operativo. |
| Licencias | Cumplido | Tabla de licencias en Anexo A y `LICENSE`. |
| Costes con cargas empresariales | Cumplido | Anexo A. |
| Sostenibilidad 600-800 palabras | Cumplido | Anexo F. |
| Bibliografía citada en texto | Cumplido | Bibliografía incluida en memoria y anexos. |
| Calidad con SonarQube/SonarCloud | Cumplido | Panel SonarCloud enlazado y documentado. |
| Releases | En revisión | Existe `v1.0.0`, pero apunta a un commit anterior a las últimas mejoras documentales. Publicar una release definitiva al cerrar los vídeos y enlaces. |

## Acciones pendientes antes de entregar

1. Sustituir las URLs pendientes de los dos vídeos en `docs/entrega/enlaces-tfg.md`.
2. Exportar `docs/entrega/enlaces-tfg.md` a PDF para UBUVirtual.
3. Comprobar `/portal` y `/health`; para consulta protegida definir antes `API_KEY`.
4. Grabar vídeo de presentación con cámara y audio.
5. Grabar vídeo de demostración funcional con portal, API y Azure Portal.
6. Publicar una release definitiva que apunte al commit final de entrega. La release `v1.0.0` existente no contiene los últimos commits de documentación.
7. Subir memoria, anexos, código y PDF de enlaces a UBUVirtual.

