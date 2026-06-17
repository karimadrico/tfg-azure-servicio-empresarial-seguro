# Guía de despliegue del TFG

**Autora:** Karima Drafli Rico  
**Universidad de Burgos**  
**Repositorio:** https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro

---

## Entorno Azure

He desplegado la solución en la suscripción **Azure for Students** de la Universidad de Burgos:

| Recurso | Nombre | Región |
|---------|--------|--------|
| Resource Group | `rg-tfg-cloudautomation-dev` | North Europe |
| App Service | `app-tfg-incidencias-dev` | Sweden Central |
| App Service Plan | `ASP-rgtfgcloudautomationdev-b089` | Sweden Central |
| Storage Account | `sttfgincidenciasdev` | Sweden Central |
| Key Vault | `kv-tfg-incidencias-dev` | Sweden Central |
| Logic App | `logic-tfg-provisionador-dev` | Sweden Central |

- **Subscription ID:** `a79fdf71-ae1e-4475-bebd-4a60a662e0ee`
- **Tenant ID:** `2aa3b0b5-a782-4f38-a898-e483b20e8d61`

---

## Paso 1 — Ejecución local

Ya validé la API en local con Git Bash:

```bash
cd src
export PATH="/c/Users/kdraf/AppData/Local/Programs/Python/Python311:/c/Users/kdraf/AppData/Local/Programs/Python/Python311/Scripts:$PATH"
export STORAGE_MODE=local
python -m pip install -r requirements.txt
python app.py
```

La API queda en `http://localhost:5000`.

---

## Paso 2 — Despliegue en Azure App Service

Desde la raíz del repositorio:

```bash
az login
bash scripts/deploy-azure.sh
```

El script publica el contenido de `src/` en `app-tfg-incidencias-dev` y configura Gunicorn como proceso de arranque.

### Comprobación en Azure

```bash
curl https://app-tfg-incidencias-dev.azurewebsites.net/
curl https://app-tfg-incidencias-dev.azurewebsites.net/health
```

Registro de incidencia con autenticación:

```bash
curl -X POST https://app-tfg-incidencias-dev.azurewebsites.net/incidencias \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tfg-api-key-ubu-2026" \
  -d '{"titulo":"Prueba cloud","descripcion":"Incidencia registrada en Azure App Service desde el despliegue del TFG","reportado_por":"karima@ubu.es"}'
```

### Despliegue con Terraform

Para reproducir la infraestructura completa:

```bash
az login
cd infra/terraform
terraform init
terraform apply -var="api_key=tfg-api-key-ubu-2026"
```

### Despliegue automatizado con GitHub Actions

```bash
bash scripts/setup-github-cicd.sh
```

Los secretos se configuran en el repositorio  
https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro  
en **Settings → Secrets and variables → Actions**:

- `AZURE_CREDENTIALS`
- `TFG_API_KEY`

Después hago push a `main` y se ejecuta `.github/workflows/deploy.yml`.

---

## Paso 3 — Logic App

Ya tengo creada la Logic App `logic-tfg-provisionador-dev` en el resource group `rg-tfg-cloudautomation-dev`.

El flujo que configure:

1. **Trigger:** petición HTTP POST con `titulo`, `descripcion` y `reportado_por`.
2. **Acción HTTP:** reenvío a `https://app-tfg-incidencias-dev.azurewebsites.net/incidencias`.
3. **Cabeceras:**
   - `Content-Type: application/json`
   - `Authorization: Bearer tfg-api-key-ubu-2026`
4. **Cuerpo:** `@triggerBody()`
5. **Respuesta:** código 201 con el JSON devuelto por la API.

Prueba del flujo:

```bash
curl -X POST "https://<url-del-trigger-logic-app>" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Incidencia desde Logic App","descripcion":"Registro automatizado de incidencia empresarial en Azure","reportado_por":"karima@ubu.es"}'
```

---

## Paso 4 — Video demostración

El guion detallado está en `docs/despliegue/guion-video.md`.

Resumen de lo que muestro en la grabación:

| Minutos | Contenido |
|---------|-----------|
| 0-1 | Presentación del TFG y problema de gestión de incidencias |
| 1-2 | Arquitectura en Azure Portal |
| 2-4 | Demo de la API con curl |
| 4-5 | Logic App `logic-tfg-provisionador-dev` |
| 5-6 | Recursos en Azure: App Service, Storage, Key Vault |
| 6-7 | Repositorio GitHub y pipeline CI/CD |
| 7-8 | Conclusiones |

---

## Paso 5 — Compilación de memoria y anexos

```bash
cd memoria
pdflatex memoria.tex
bibtex memoria
pdflatex memoria.tex
pdflatex memoria.tex

pdflatex anexos.tex
bibtex anexos
pdflatex anexos.tex
pdflatex anexos.tex
```

Se generan `memoria.pdf` y `anexos.pdf`.
