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
```

## Componente de IA ligera

El clasificador de `src/classifier.py`:

- detecta tipo de solicitud;
- asigna prioridad;
- clasifica categoría;
- genera recomendación operativa;
- devuelve un nivel de confianza.

No requiere Azure OpenAI, por lo que se ajusta mejor al alcance académico y al presupuesto Azure for Students.

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

