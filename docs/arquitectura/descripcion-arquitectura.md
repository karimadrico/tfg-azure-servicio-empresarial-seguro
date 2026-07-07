# Arquitectura del sistema

El sistema se basa en una arquitectura cloud desplegada en Microsoft Azure.

Componentes principales:

- Azure App Service
  - Ejecuta la API Python del sistema

- Azure Cosmos DB
- Azure Storage Account como soporte de migración
  - Conserva evidencias de la persistencia inicial y sirve como soporte de migración

- Azure Key Vault
  - Gestión segura de secretos y credenciales

- Azure Monitor y logs de App Service
  - Revisión básica del estado operativo y registros del despliegue

## Flujo del sistema

1. El usuario crea una incidencia.
2. La API procesa la solicitud.
3. El sistema clasifica la incidencia.
4. La incidencia se almacena en Azure Cosmos DB como documento JSON.
5. El endpoint `/health`, los logs de App Service y Azure Portal permiten verificar el funcionamiento del sistema.

