# TFG - Servicio Empresarial Seguro en Microsoft Azure

**Autor:** Karima Drafli Rico  
**Universidad de Burgos**  
**Tutor:** D. José Ignacio Santos Martín

## Descripción

Sistema cloud para la gestión automatizada de incidencias empresariales en Microsoft Azure. Incluye API REST en Flask, persistencia en Blob Storage, gestión segura de secretos con Key Vault, clasificación automática de incidencias y automatización mediante Logic App.

## Arquitectura

- **Azure App Service** — API Flask (Python 3.11)
- **Azure Blob Storage** — persistencia de incidencias
- **Azure Key Vault** — token de autenticación
- **Azure Logic App** — registro automatizado de incidencias
- **GitHub Actions** — CI/CD (tests + Terraform + despliegue)

## Estructura del repositorio

```
src/                  API Flask
tests/                Pruebas unitarias
infra/terraform/      Infraestructura como código
logicapp/             Logic App de automatización
memoria/              Memoria y anexos LaTeX
docs/                 Documentación técnica
pipelines/            Azure DevOps pipelines
```

## Ejecución local

```bash
cd src
pip install -r requirements.txt
set STORAGE_MODE=local
python app.py
```

API disponible en `http://localhost:5000`.

## Pruebas

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Despliegue en Azure

1. Configurar secretos en GitHub: `AZURE_CREDENTIALS`, `TFG_API_KEY`
2. Push a `main` → GitHub Actions despliega infraestructura y API
3. URL de la API: `https://app-tfg-incidencias-dev.azurewebsites.net`
4. Importar Logic App desde `logicapp/logicapp-workflow.json`

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado del servicio |
| GET | `/health` | Salud del sistema |
| GET | `/incidencias` | Listar incidencias |
| POST | `/incidencias` | Crear incidencia |
| GET | `/metricas` | Métricas agregadas |

## Backlog

https://zube.io/tfg-azure-servicio-empresarial/tfg-servicio-empresarial-seguro/w/workspace-1/kanban
