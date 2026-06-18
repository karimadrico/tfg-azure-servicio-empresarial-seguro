# Estado Actual del Proyecto

Última actualización: 18 de junio de 2026

Porcentaje completado: ~90%

## Resumen Ejecutivo

El proyecto dispone de una solución funcional desplegada en Microsoft Azure: API Flask con gestión de solicitudes TI, portal web, clasificación automática, persistencia en Azure Blob Storage, gestión de secretos con Key Vault, Managed Identity y despliegue reproducible mediante PowerShell y Azure CLI.

Quedan como tareas finales la grabación de los dos vídeos obligatorios, la generación del PDF final de enlaces y la creación de la release final del repositorio.

## Estado por Componentes

### Completados

- API Flask (`src/app.py`): endpoints operativos con validación y autenticación Bearer.
- Portal web (`src/static/index.html`): formulario de solicitud y experiencia de demostración.
- Clasificador automático (`src/classifier.py`): prioridad, tipo, categoría y recomendación.
- Persistencia (`src/storage.py`): modo local y Azure Blob Storage.
- Seguridad: Key Vault, Managed Identity y token Bearer.
- Despliegue Azure: `scripts/deploy-azure.ps1` y verificación con `scripts/verify-azure.ps1`.
- Pruebas unitarias (`tests/test_api.py`).
- Planificación: cinco sprints en Zube con enlace en README y anexos.
- Calidad: SonarCloud manual con Quality Gate aprobado.
- Memoria y anexos en LaTeX/PDF.

### Pendientes de entrega

- Grabar vídeo de presentación del TFG con cámara y audio.
- Grabar vídeo de demostración funcional del producto.
- Crear PDF final de enlaces para UBUVirtual.
- Crear release final en GitHub.
- Guardar capturas finales: Azure Portal, Zube, SonarCloud y aplicación desplegada.

## Checklist de Evaluación

| Criterio | Estado |
|----------|--------|
| Planificación y seguimiento | Cumplido: Zube, sprints, commits y documentación |
| Análisis, diseño e implementación | Cumplido: API, portal, Azure, seguridad, pruebas y despliegue |
| Producto software evaluable | Cumplido: portal y API desplegados en Azure App Service |
| Calidad de código | Cumplido: SonarCloud enlazado y documentado |
| Defensa | Pendiente: vídeos y presentación oral |

## URLs clave

- Portal: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
- API: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net
- Zube: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban
- SonarCloud: https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

