# Arquitectura del sistema

El sistema se basa en una arquitectura cloud desplegada en Microsoft Azure.

Componentes principales:

- Azure App Service
  - Ejecuta la API Python del sistema

- Azure Storage Account
  - Almacena incidencias y documentos

- Azure Key Vault
  - Gestión segura de secretos y credenciales

- Azure Monitor y logs de App Service
  - Revisión básica del estado operativo y registros del despliegue

## Flujo del sistema

1. El usuario crea una incidencia.
2. La API procesa la solicitud.
3. El sistema clasifica la incidencia.
4. La incidencia se almacena en Azure Storage.
5. El endpoint `/health`, los logs de App Service y Azure Portal permiten verificar el funcionamiento del sistema.
