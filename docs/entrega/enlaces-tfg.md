# Enlaces para UBUVirtual

Este documento sirve como base para generar el PDF final de enlaces solicitado en la entrega.

## Enlaces obligatorios

| Recurso | URL |
|---------|-----|
| Repositorio GitHub | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro |
| Vídeo de presentación | https://youtu.be/f2bxGQOfg5o |
| Vídeo de demostración funcional | Pendiente de grabar y publicar |

## Enlaces aportados

| Recurso | URL |
|---------|-----|
| Portal desplegado | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal |
| API desplegada | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net |
| Estado de la API | https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health |
| Zube | https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban |
| SonarCloud | https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro |
| Release publicada | https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro/releases/tag/v1.2.0 |

## Datos de acceso para la prueba

Las operaciones públicas del portal permiten registrar solicitudes sin credenciales. Las operaciones de equipo TI, centro operativo, exportación, demostración y OpenAPI protegida requieren un token Bearer.

El token de evaluación se facilita únicamente en el PDF privado de enlaces entregado en UBUVirtual y corresponde al secreto `api-key` almacenado en Azure Key Vault (`kv-tfg-incidencias-dev`). No se incluye en el repositorio público, en vídeos ni en capturas de evidencias.

Formato de uso:

```text
Authorization: Bearer <token-de-evaluacion>
```

## Persistencia cloud

La aplicación desplegada utiliza Azure Cosmos DB como base de datos documental. El endpoint público /health permite comprobar que el modo de almacenamiento activo es cosmos. Las solicitudes existentes se migraron desde Blob Storage mediante el script de migración del repositorio.
