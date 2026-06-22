# Documentación de despliegue

Esta carpeta describe cómo desplegar y demostrar la solución Azure del TFG.

| Fichero | Uso |
|---------|-----|
| `guia-azure-paso-a-paso.md` | Despliegue rápido con Azure CLI, App Service, Key Vault, Storage y Logic App. |
| `guia-completa.md` | Guía completa de ejecución local, despliegue, verificación y compilación LaTeX. |

La verificación completa con `scripts/verify-azure.ps1` requiere definir previamente `API_KEY` en la sesión local. Los endpoints públicos `/`, `/health` y `/portal` pueden comprobarse sin token.
