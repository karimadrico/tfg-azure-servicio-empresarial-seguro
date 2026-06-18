# Logic App de solicitudes TI

Esta carpeta contiene la definicion del flujo de automatizacion empresarial del TFG.

El flujo realiza:

1. Recibe una solicitud por HTTP.
2. Valida que existan `titulo`, `descripcion` y `reportado_por`.
3. Llama a la API desplegada en Azure App Service mediante `POST /solicitudes`.
4. Devuelve al cliente la respuesta de la API con identificador, prioridad, clasificacion y recomendacion.

La plantilla principal esta en `infra/bicep/logicapp.bicep`. El fichero `workflow.json` sirve como referencia funcional del flujo para revision o importacion manual en Azure Portal.

No se almacena ninguna clave en el repositorio. La clave se pasa como parametro seguro durante el despliegue.
