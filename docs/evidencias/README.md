# Evidencias finales del TFG

Esta carpeta contiene capturas propias utilizadas para demostrar que el prototipo existe, está desplegado, funciona y ha seguido un proceso de desarrollo controlado. Las imágenes complementan la memoria, los anexos y la defensa oral.

## 1. Recursos Azure desplegados

### Resource Group

![Resource Group final](azure-resource-group-final.png)

La captura muestra el grupo de recursos `rg-tfg-cloudautomation-dev` con los recursos principales del despliegue: App Service, Storage Account, Key Vault y App Service Plan. Sirve como evidencia de que la solución no es solo código local, sino una instancia real organizada en Azure.

### App Service

![Overview App Service](azure-app-service-overview.png)

La captura recoge el App Service `app-tfg-incidencias-dev`, su estado operativo y la URL pública. Es la evidencia principal del despliegue web usado por el tribunal.

![Configuración App Service](azure-app-service-configuration.png)

La captura muestra la configuración de la aplicación con variables como `STORAGE_MODE`, `KEY_VAULT_URL` y `AZURE_STORAGE_CONTAINER`. No debe exponer valores secretos completos; su objetivo es evidenciar la configuración cloud.

### Identidad administrada

![Managed Identity](azure-managed-identity.png)

La identidad administrada del App Service permite acceder a Key Vault sin guardar credenciales en el código. La captura `azure-managed-identity - copia.png` es una copia de apoyo y no es necesaria para la entrega principal.

### Key Vault

![Overview Key Vault](azure-key-vault-overview.png)

La captura muestra el Key Vault `kv-tfg-incidencias-dev`, usado para centralizar secretos.

![Secreto API Key](azure-key-vault-secret.png)

La captura evidencia la existencia del secreto `api-key` sin mostrar su valor. Se utiliza para justificar la separación de secretos respecto al repositorio.

### Storage Account

![Storage Account](azure-storage-container.png)

La captura muestra el Storage Account `sttfgincidenciasdev` y el contenedor `incidencias`.

![Blob JSON](azure-storage-container-blob-json.png)

La captura muestra el blob JSON usado para persistir las solicitudes. Es útil para explicar el modelo documental empleado en lugar de una base de datos relacional.

## 2. Portal y API funcionando

![Portal Home](url-portal-home.png)

Pantalla del portal desplegado en `/portal`, con el formulario de solicitud TI.

![Portal solicitud enviada](portal-solicitud-enviada.png)

Evidencia funcional del envío de una solicitud desde el portal. Debe verse la respuesta con identificador, prioridad, clasificación y recomendación.

![Respuesta JSON portal](portal-solicitud-enviada-json.png)

Variante de la evidencia anterior centrada en la respuesta JSON generada por la API.

![Health check](url-portal-health.png)

Captura de `/health`, mostrando que el servicio responde y que el modo de almacenamiento es `azure`.

![Solicitudes protegidas](api-solicitudes-protegidas.png)

Evidencia de `GET /solicitudes` con autenticación Bearer. Demuestra que la consulta está protegida y devuelve datos reales.

![Métricas API](api-metricas.png)

Evidencia de `GET /metricas`, con agregados por estado, prioridad y tipo de solicitud.

![Verificación Azure](azure-verification-script.png)

Salida de `scripts/verify-azure.ps1`, que valida automáticamente `/`, `/health`, creación de solicitud, listado y métricas.

## 2.1. Automatizacion con Logic App

La Logic App `logic-tfg-solicitudes-dev` automatiza la entrada de solicitudes externas mediante un trigger HTTP y una llamada a la API desplegada en App Service. Las evidencias conservadas en esta carpeta son:

- `logic-app-workflow.png`: vista general del disenador con trigger HTTP, accion de creacion de solicitud y respuesta final.
- `logic-app-workflow-solicitud.png`: detalle del paso que envia la solicitud hacia `POST /solicitudes`.
- `logic-app-workflow-cliente.png`: detalle de la respuesta enviada al cliente que invoca el flujo.
- `logic-app-run-history.png`: historial de ejecucion correcto al enviar una solicitud.
- `logic-app-run-history-solicitud.png`: salida de la accion que crea la solicitud, con cabeceras sensibles ocultas.
- `logic-app-run-history-respondercliente.png`: respuesta final devuelta por la Logic App.

Estas evidencias sirven para defender la automatizacion cloud del proceso empresarial. No deben mostrar firmas `sig`, claves Bearer ni valores de secretos.

## 2.2. Observabilidad con Azure Monitor

Application Insights y Azure Monitor permiten justificar que el prototipo no solo se despliega, sino que tambien puede supervisarse durante su ejecucion.

Evidencias incorporadas para completar la observabilidad:

- `application-insights-overview.png`: vista general del recurso `appi-tfg-incidencias-dev`.
- `azure-monitor-metrics.png`: metricas del App Service o de Application Insights, por ejemplo peticiones, errores o tiempo de respuesta.

## 3. Calidad de código

![Quality Gate SonarCloud](sonarcloud-quality-gate.png)

Captura del Quality Gate aprobado en SonarCloud. Es la evidencia principal para el criterio de calidad interna.

Evidencia final incorporada:

- `sonarcloud-quality-gate-final-20junio.png`: estado más reciente, con Quality Gate aprobado, seguridad A, cero issues de seguridad y ocho issues no bloqueantes de mantenibilidad.

![Issues SonarCloud](sonarcloud-issues.png)

Resumen de issues y calificaciones de SonarCloud. Sirve para explicar qué se corrigió y qué queda como mejora posterior.

## 4. Seguimiento del proyecto

![Sprints cerrados Zube](zube-sprints-closed.png)

Evidencia de sprints cerrados en Zube. Para más detalle del seguimiento por iteraciones se conserva además la carpeta `docs/sprints/`, con capturas históricas y el resumen de sprints.

![Sprint abierto Zube](zube-sprints-open.png)

Evidencia del Sprint 5 orientado al cierre de memoria, anexos, vídeos, release y entrega.

![Kanban final Zube](zube-kanban-final.png)

Vista del tablero Kanban final, útil para demostrar el estado del trabajo en la defensa.

## 5. Repositorio y entrega

![README GitHub](github-repo-readme.png)

Captura de la página principal del repositorio en GitHub, mostrando que el README funciona como landing page del proyecto.

![Commits GitHub](github-commits.png)

Evidencia del historial de commits y de la trazabilidad del desarrollo.

![Release final GitHub](github-release-final.png)

Captura de la release final `v1.0.0`, utilizada para distribuir el estado entregado del repositorio.

## 6. Capturas complementarias

![Web App](web-app.png)

Captura complementaria de la aplicación web en Azure.

![Portal Home adicional](url-portal-home.png)

Captura adicional del portal público usado para la demostración.


