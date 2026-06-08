# Logic App - Automatización de incidencias

Esta Logic App actúa como punto de entrada automatizado para registrar incidencias en la API del TFG.

## Flujo

1. Recibe una petición HTTP manual con `titulo`, `descripcion` y `reportado_por`.
2. Reenvía la incidencia a `POST /incidencias` de la API Flask.
3. Devuelve la respuesta de la API al solicitante.

## Despliegue en Azure Portal

1. Crear una Logic App en el resource group `rg-tfg-cloudautomation-dev`.
2. Importar el flujo desde `logicapp-workflow.json` o recrearlo con el diseñador visual.
3. Configurar los parámetros:
   - `apiBaseUrl`: `https://app-tfg-incidencias-dev.azurewebsites.net`
   - `apiKey`: valor del secreto `api-key` en Key Vault.
4. Guardar y activar el flujo.
5. Copiar la URL del trigger HTTP manual para pruebas.

## Ejemplo de prueba

```bash
curl -X POST "https://<logic-app-url>/manual/paths/invoke?api-version=2016-10-01&sp=..." \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Servidor caído",
    "descripcion": "El servidor principal no responde desde esta mañana",
    "reportado_por": "usuario@empresa.com"
  }'
```
