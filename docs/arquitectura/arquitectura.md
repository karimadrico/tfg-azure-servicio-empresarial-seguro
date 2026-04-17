# Arquitectura del Sistema

## 1. Descripción General

El sistema desarrollado en este TFG implementa una plataforma cloud para la **automatización segura de procesos empresariales** en Microsoft Azure, con especial énfasis en:

- **Gestión de secretos y credenciales** centralizada
- **Automatización de procesos** (especialmente gestión de incidencias)
- **Seguridad** como principio fundamental
- **Monitorización** y trazabilidad de operaciones
- **Clasificación inteligente** de incidencias mediante componentes de IA

## 2. Componentes Principales

### 2.1 Capa de Aplicación

**Azure App Service** (Python 3.14 + Flask)
- Ejecuta la API REST del sistema
- Maneja las operaciones de negocio
- Expone endpoints para crear, consultar y procesar incidencias
- SKU: Plan gratuito (infraestructura compartida en Linux)

### 2.2 Capa de Seguridad

**Azure Key Vault**
- Almacena centralizadamente secretos y credenciales
- Gestión de permisos mediante identidades administradas
- Previene hardcoding de credenciales en código
- Auditoría completa de accesos

### 2.3 Capa de Almacenamiento

**Azure Storage Account**
- Almacenamiento de blobs para datos de incidencias
- Recuperación y análisis histórico
- Escalabilidad automática

### 2.4 Monitorización y Observabilidad

**Application Insights** (opcional)
- Monitorización de rendimiento
- Detección de anomalías
- Análisis de logs y trazas

## 3. Flujo Arquitectónico

```
Usuario/Sistema Externo
    ↓
    → API REST en App Service
    ↓
    → Validación de credenciales (Key Vault)
    ↓
    → Procesa incidencia
    ↓
    → Clasificación automática
    ↓
    → Almacenamiento en Storage
    ↓
    → Generación de métricas
    ↓
    → Respuesta al usuario
```

## 4. Decisiones Arquitectónicas

### 4.1 Python + Flask
- Rapidez de prototipado
- Flexibilidad para integración con Azure
- Comunidad amplia y documentación abundante

### 4.2 API REST
- Estándar de la industria
- Integración en cualquier tipo de sistema
- Facilita testing y validación

### 4.3 Azure como proveedor cloud
- Servicios gestionados (reducen overhead operacional)
- Integración nativa con identidades (Entra ID)
- Características de seguridad enterprise
- Plan gratuito para estudiantes

## 5. Requisitos No Funcionales

- **Seguridad**: gestión centralizada de secretos y credenciales con Azure Key Vault, evitando configuración insegura en el código. Estado: implementado.
- **Escalabilidad**: la arquitectura se basa en Azure App Service y Storage, diseñados para soportar un aumento de solicitudes sin cambios significativos en la aplicación.
- **Disponibilidad**: el despliegue se apoya en Azure y en flujos de CI/CD para entregas automáticas. Estado: en progreso.
- **Trazabilidad**: se recopilan logs y métricas para supervisar el comportamiento de la API y los procesos de negocio. Estado: en progreso.
- **Rendimiento**: respuesta objetivo de la API inferior a 1 segundo en operaciones habituales. Estado: validado en pruebas de funcionalidad.

## 6. Arquitectura de Componentes

La solución se organiza en los siguientes bloques:

- El cliente o sistema externo interactúa con la API REST expuesta por Azure App Service.
- El servicio Flask recibe las solicitudes, aplica la lógica de negocio y consulta los secretos de acceso en Azure Key Vault.
- Las incidencias y los datos persistentes se almacenan en Azure Storage Account, con acceso controlado y auditoría.
- Application Insights recoge métricas, logs y trazas para observabilidad y análisis continuo.

El conjunto produce una arquitectura segura y gestionable, donde cada componente asume un rol claro:

- App Service: procesamiento de solicitudes y enrutamiento de endpoints.
- Key Vault: custodia de credenciales y control de accesos.
- Storage Account: almacenamiento duradero y recuperación de datos.
- Application Insights: monitorización y trazabilidad de la operación.

## 7. Tecnologías Clave

- **Azure App Service**: plataforma gestionada que aloja la API y simplifica el despliegue continuo.
- **Python 3.14**: versión moderna y adecuada para el desarrollo de APIs en Flask.
- **Flask 2.x**: framework ligero y flexible, ideal para prototipos que requieren integración rápida.
- **Azure**: proveedor cloud elegido por sus capacidades de seguridad, gestión de identidades y servicios empresariales.
- **GitHub Actions**: canal de CI/CD integrado con el repositorio para automatizar pruebas y despliegues.
- **Git**: control de versiones para gestionar cambios en el proyecto y colaborar de forma ordenada.

## 8. Consideraciones de Seguridad

1. **No hardcodear secretos** → Usamos Key Vault
2. **Autenticación** → Identidades administradas de Azure
3. **Autorización** → RBAC en Key Vault y Storage
4. **Auditoría** → Logs de todas las operaciones
5. **Encriptación** → En tránsito (HTTPS) y en reposo (Storage)

## 9. Plan de Escalabilidad

- **App Service**: Pasar de SKU gratuito → Standard si es necesario
- **Storage**: Escalabilidad automática integrada
- **Key Vault**: Sin límites de escalabilidad
- **Monitoring**: Application Insights para análisis de capacidad

## 10. Próximas Iteraciones

- Integración de Azure Functions para lógica asíncrona
- Machine Learning para clasificación avanzada
- Dashboard real-time con Power BI
- API Gateway para control de tráfico
