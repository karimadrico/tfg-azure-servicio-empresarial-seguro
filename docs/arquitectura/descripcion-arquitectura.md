# Arquitectura del sistema

El sistema se basa en una arquitectura cloud desplegada en Microsoft Azure.

Componentes principales:

- Azure App Service
  - Ejecuta la API Python del sistema

- Azure Storage Account
  - Almacena incidencias y documentos

- Azure Key Vault
  - Gestión segura de secretos y credenciales

- Application Insights
  - Monitorización y telemetría de la aplicación

## Flujo del sistema

1. El usuario crea una incidencia.
2. La API procesa la solicitud.
3. El sistema clasifica la incidencia.
4. La incidencia se almacena en Azure Storage.
5. Application Insights monitoriza el funcionamiento del sistema.