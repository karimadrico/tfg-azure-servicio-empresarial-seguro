# Arquitectura de la plataforma TFG

## Proceso empresarial

Automatización de solicitudes internas de TI:

| Tipo | Ejemplo |
|------|---------|
| Acceso | VPN, permisos, cuentas |
| Entorno | Staging, desarrollo, producción |
| Aplicación | Alta de servicio o API |
| Configuración | Cambio de parámetros |
| Incidencia | Fallo operativo |

## Flujo arquitectónico

```text
Empleado / Tribunal
        |
        v
Portal web en App Service
        |
        v
API Flask
        |
        +--> Clasificador ligero
        |
        +--> Blob Storage
        |
        +--> Key Vault mediante Managed Identity

Sistema externo
        |
        v
Logic App
        |
        v
POST /solicitudes
```

## Clasificación automática basada en reglas

El clasificador de `src/classifier.py`:

- detecta tipo de solicitud;
- asigna prioridad;
- clasifica categoría;
- genera recomendación operativa;
- devuelve un nivel de confianza.

No requiere un servicio de lenguaje externo ni un conjunto de entrenamiento. Las decisiones pueden seguirse en el código y repetirse en las pruebas.

## Automatizacion con Logic App

La Logic App `logic-tfg-solicitudes-dev` recibe solicitudes por HTTP y las reenvia a `POST /solicitudes`. Esta pieza permite demostrar un flujo de automatizacion empresarial sin que el sistema externo tenga que conocer los detalles internos de la API Flask.

## Seguridad

- Token Bearer para operaciones protegidas.
- Token almacenado en Azure Key Vault.
- Acceso desde App Service mediante Managed Identity.
- Blob Storage privado.
- Variables sensibles fuera del código fuente.

## Despliegue

- Script operativo: `scripts/deploy-azure.ps1`.
- Verificación: `scripts/verify-azure.ps1`.
- Infraestructura documentada: `infra/terraform/` e `infra/bicep/`.

