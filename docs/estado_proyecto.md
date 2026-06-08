# Estado Actual del Proyecto

Última actualización: 8 de junio de 2026

Porcentaje completado: ~85%

## 1. Resumen Ejecutivo

El proyecto dispone de una solución funcional implementada: API Flask con gestión de incidencias, clasificación automática, persistencia en Azure Storage, gestión de secretos con Key Vault, infraestructura Terraform consolidada, CI/CD con GitHub Actions, Logic App de automatización y documentación actualizada en memoria y anexos.

Pendiente para entrega final: despliegue verificado en Azure, video demostración y compilación final de memoria/anexos PDF.

## 2. Estado por Componentes

### Completados

- API Flask (`src/app.py`): endpoints operativos con validación y autenticación Bearer.
- Clasificador automático (`src/classifier.py`): prioridad y categoría por análisis de palabras clave.
- Persistencia (`src/storage.py`): modo local y Azure Blob Storage.
- Pruebas unitarias (`tests/test_api.py`).
- Terraform consolidado (`infra/terraform/`): App Service, Storage, Key Vault, Managed Identity.
- CI/CD GitHub Actions: tests + Terraform + despliegue de `src/`.
- Logic App: flujo HTTP → API documentado en `logicapp/`.
- Memoria y anexos LaTeX actualizados (capítulos 5, B, C, D, E).
- Documentación técnica (`docs/`, `README.md`).

### En progreso

- Despliegue final en Azure (requiere credenciales `AZURE_CREDENTIALS` en GitHub).
- Importación de Logic App en portal Azure.
- Video demostración y presentación personal.

### Planificado

- Application Insights para monitorización avanzada.
- Interfaz web de usuario.
- Modelo ML para clasificación (mejora futura).

## 3. Checklist de Evaluación (Tribunal)

| Criterio | Estado |
|----------|--------|
| Planificación (25%) | Plan, sprints, Zube, commits — ~90% |
| Análisis, diseño e implementación (40%) | API funcional, Terraform, pruebas, despliegue — ~85% |
| Presentación y defensa (35%) | Memoria en progreso, videos pendientes — ~60% |

## 4. Próximos pasos inmediatos

1. Configurar secretos en GitHub y ejecutar pipeline de despliegue.
2. Probar API en `https://app-tfg-incidencias-dev.azurewebsites.net`.
3. Importar y probar Logic App.
4. Grabar video demostración (5-10 min).
5. Compilar `memoria.tex` y `anexos.tex` a PDF final.
