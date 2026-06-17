# Logic App — logic-tfg-solicitudes-dev

Orquestador del flujo de solicitudes TI empresariales.

## Flujo

```text
Solicitud HTTP
    ↓
Registrar en API (/solicitudes)
    ↓
Clasificación IA + recomendación
    ↓
Construir notificación
    ↓
Respuesta JSON al solicitante
```

## Despliegue en Azure Portal

1. Ir a **Logic App** → **Create** → nombre: `logic-tfg-solicitudes-dev`
2. Región: **Sweden Central**, plan: **Consumption**
3. En **Logic app code view**, pegar el contenido de `workflow.json` (sección `definition`)
4. Guardar y copiar la **URL del trigger HTTP**

## Prueba

```bash
curl -X POST "https://<URL-TRIGGER-LOGIC-APP>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_solicitud": "acceso",
    "titulo": "Solicitud acceso VPN",
    "descripcion": "Necesito acceso VPN al entorno de desarrollo para el proyecto cloud",
    "reportado_por": "karima@ubu.es"
  }'
```

## Cabeceras hacia la API

- `Content-Type: application/json`
- `Authorization: Bearer <api-key-desde-key-vault>`

## Nota sobre email

El paso de notificación genera el mensaje en JSON. Para envío real de correo, conectar el conector **Office 365 Outlook** o **Gmail** en el diseñador de Logic Apps.
