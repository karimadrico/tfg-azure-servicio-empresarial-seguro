# Infraestructura Cloud en Azure

El sistema se despliega en Microsoft Azure utilizando los siguientes recursos.

## Resource Group

`rg-tfg-cloudautomation-dev`

## Recursos principales

### App Service

`app-tfg-incidencias-dev`

Servicio encargado de ejecutar la API desarrollada en Python.

### Storage Account

`sttfgincidenciasdev`

Se utilizará para almacenar información relacionada con incidencias y documentos.

### Azure Key Vault

`kv-tfg-incidencias-dev`

Servicio utilizado para la gestión segura de secretos y credenciales.

### Managed Identity

Identidad administrada del App Service utilizada para acceder a Key Vault sin almacenar credenciales en el código.

### Observabilidad

La verificación operativa se realiza mediante el endpoint `/health`, los logs de App Service y las métricas básicas disponibles en Azure Portal. Application Insights queda identificado como una mejora futura, no como componente activo de la entrega.
