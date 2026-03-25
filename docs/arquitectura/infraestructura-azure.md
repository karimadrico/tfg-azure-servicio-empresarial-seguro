# Infraestructura Cloud en Azure

El sistema se despliega en Microsoft Azure utilizando los siguientes recursos.

## Resource Group

tfg-empresa-rg

## Recursos principales

### App Service

tfg-servicio-empresarial

Servicio encargado de ejecutar la API desarrollada en Python.

### Storage Account

tfgempresastorage

Se utilizará para almacenar información relacionada con incidencias y documentos.

### Azure Key Vault

tfg-empresa-keyvault

Servicio utilizado para la gestión segura de secretos y credenciales.

### Application Insights

Sistema de monitorización para analizar el rendimiento de la aplicación.