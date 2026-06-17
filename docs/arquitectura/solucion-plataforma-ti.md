# Arquitectura de la plataforma TFG

## Proceso empresarial

Automatización de **solicitudes internas de TI** en una empresa:

| Tipo | Ejemplo |
|------|---------|
| Acceso | VPN, permisos, cuentas |
| Entorno | Staging, desarrollo, producción |
| Aplicación | Alta de servicio o API |
| Configuración | Cambio de parámetros |
| Incidencia | Fallo operativo |

## Patrón arquitectónico

Replica el patrón de orquestación corporativa (solicitud → validación → automatización → notificación) sin depender de Jenkins, ADO ni suscripciones corporativas.

```text
Empleado / Portal Web
        |
        v
+------------------+
|   Logic App      |  Trigger HTTP
+------------------+
        |
        v
+------------------+
|   API Flask      |  Clasificación IA + recomendación
+------------------+
        |
   +----+----+
   |         |
   v         v
Storage   Key Vault
(Blob)    (api-key)
```

## Componente de IA

Clasificador ligero en `src/classifier.py`:

- Detecta **tipo de solicitud**
- Asigna **prioridad** (baja/media/alta)
- Clasifica **categoría** (seguridad/infraestructura/soporte)
- Genera **recomendación operativa**

No requiere Azure OpenAI (coste/cuota estudiante). Cumple el objetivo TFG de "componente básico de IA como valor añadido".

## Seguridad

- Token Bearer en Key Vault
- Managed Identity en App Service
- Blob Storage privado
- Lecturas protegidas con autenticación

## Despliegue

- **Terraform:** `infra/terraform/`
- **Bicep:** `infra/bicep/`
- **Script:** `scripts/deploy-azure.ps1`

## URLs de demostración

- API: https://app-tfg-incidencias-dev.azurewebsites.net
- Portal: https://app-tfg-incidencias-dev.azurewebsites.net/portal
- Health: https://app-tfg-incidencias-dev.azurewebsites.net/health
