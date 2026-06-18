# Guion del video de demostración

**TFG:** Cloud Computing: Análisis, Diseño y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure  
**Autora:** Karima Drafli Rico — Universidad de Burgos  
**Duración máxima:** 5 minutos

## 1. Introducción

Presentar el problema: muchas solicitudes internas de TI se gestionan con correos, hojas de cálculo o procesos poco trazables. El prototipo centraliza solicitudes, las clasifica automáticamente y las almacena de forma segura en Azure.

## 2. Arquitectura en Azure Portal

Mostrar el resource group `rg-tfg-cloudautomation-dev` y los recursos:

- `app-tfg-incidencias-dev`: API Flask y portal web en App Service.
- `sttfgincidenciasdev`: Storage Account para persistencia.
- `kv-tfg-incidencias-dev`: Key Vault para el token de autenticación.
- Managed Identity del App Service.
- `logic-tfg-solicitudes-dev`: automatización externa de solicitudes.
- `appi-tfg-incidencias-dev`: observabilidad con Application Insights.

## 3. Demostración funcional

Abrir:

```text
https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
```

Crear una solicitud desde el portal y explicar que el sistema devuelve prioridad, clasificación y recomendación. Después, mostrar brevemente que la Logic App permite recibir una solicitud externa y llamar al mismo endpoint `POST /solicitudes`.

## 4. Prueba técnica de API

Mostrar en PowerShell:

```powershell
$base = "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net"
$headers = @{ Authorization = "Bearer $env:API_KEY" }

Invoke-RestMethod "$base/health"
Invoke-RestMethod "$base/solicitudes" -Headers $headers
Invoke-RestMethod "$base/metricas" -Headers $headers
```

## 5. Repositorio, Zube y SonarCloud

Mostrar:

- README con enlaces de evaluación.
- `src/`, `tests/`, `scripts/`, `infra/` y `memoria/`.
- Zube con los cinco sprints.
- SonarCloud con Quality Gate aprobado.

## 6. Cierre

Cerrar explicando que el trabajo cubre análisis, diseño, implementación, pruebas, despliegue cloud, seguridad con Key Vault, seguimiento ágil y calidad de código.

