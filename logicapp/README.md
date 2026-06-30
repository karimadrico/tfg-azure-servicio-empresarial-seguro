# Logic App de solicitudes TI

Esta carpeta contiene la definición del flujo de automatización empresarial utilizado en el TFG.

## Función dentro de la solución

La Logic App representa un canal de entrada desde otros sistemas de la empresa. Por ejemplo, una intranet, un formulario corporativo o una herramienta externa puede enviar una solicitud HTTP sin conocer la estructura interna del portal. La Logic App recibe esa petición y la reenvía a la API desplegada en Azure App Service.

## Flujo implementado

1. Recibe una solicitud por HTTP.
2. Construye el cuerpo esperado por `POST /solicitudes`.
3. Invoca la API desplegada en App Service usando token Bearer.
4. La API valida, clasifica, calcula prioridad/SLA y persiste en Cosmos DB.
5. La Logic App devuelve al cliente la respuesta generada por la API.

La Logic App no accede directamente a Cosmos DB ni duplica reglas de negocio. Toda la validación y persistencia queda centralizada en la API Flask.

## Archivos relacionados

- `workflow.json`: definición funcional del flujo.
- `infra/bicep/logicapp.bicep`: plantilla de infraestructura asociada.
- `scripts/deploy-logicapp.ps1`: despliegue operativo desde PowerShell.

No se almacena ninguna clave en el repositorio. El token se pasa como parámetro seguro durante el despliegue y se conserva como secreto en Azure Key Vault.
