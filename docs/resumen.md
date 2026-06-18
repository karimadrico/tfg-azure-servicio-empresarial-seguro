# Resumen del proyecto

El TFG desarrolla una plataforma cloud para registrar, clasificar y consultar solicitudes operativas TI en Microsoft Azure. El prototipo final está desplegado en Azure App Service e integra persistencia en Azure Blob Storage, gestión de secretos con Azure Key Vault, Managed Identity, autenticación Bearer, un portal web y una API Flask.

## Alcance entregado

- Portal web accesible desde Azure App Service.
- API REST para crear solicitudes, consultar solicitudes protegidas y obtener métricas.
- Clasificador ligero para tipo de solicitud, prioridad, categoría y recomendación.
- Persistencia cloud en Azure Blob Storage y modo local para pruebas.
- Secreto de API gestionado con Azure Key Vault.
- Despliegue reproducible con `scripts/deploy-azure.ps1`.
- Verificación automatizada con `scripts/verify-azure.ps1`.
- Pruebas unitarias en `tests/test_api.py`.
- Seguimiento del trabajo en Zube.
- Calidad revisada en SonarCloud.

## Recursos principales

- Repositorio: https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro
- Portal: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
- API: https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net
- Zube: https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban
- SonarCloud: https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

## Entregables documentales

- Memoria: `memoria/memoria.pdf`
- Anexos: `memoria/anexos.pdf`
- Evidencias: `docs/`
- Infraestructura declarativa de apoyo: `infra/terraform/` y `infra/bicep/`
