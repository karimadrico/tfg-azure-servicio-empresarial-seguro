# Guía completa de despliegue del TFG

**Autora:** Karima Drafli Rico  
**Universidad de Burgos**  
**Repositorio:** https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro

## Entorno Azure

La solución se ha desplegado en la suscripción Azure for Students:

| Recurso | Nombre | Región |
|---------|--------|--------|
| Resource Group | `rg-tfg-cloudautomation-dev` | Sweden Central |
| App Service | `app-tfg-incidencias-dev` | Sweden Central |
| App Service Plan | `ASP-rgtfgcloudautomationdev-b089` | Sweden Central |
| Storage Account | `sttfgincidenciasdev` | Sweden Central |
| Key Vault | `kv-tfg-incidencias-dev` | Sweden Central |

## Ejecución local

```powershell
cd src
$env:STORAGE_MODE = "local"
python -m pip install -r requirements.txt
python app.py
```

La API queda en `http://localhost:5000` y el portal en `http://localhost:5000/portal`.

## Despliegue operativo

Desde la raíz:

```powershell
az login
.\scripts\deploy-azure.ps1
```

El despliegue utilizado en la entrega configura App Service, Storage, Key Vault, Managed Identity y publica el código de `src/`.

## Verificación

```powershell
.\scripts\verify-azure.ps1
```

También se pueden verificar manualmente:

```powershell
Invoke-RestMethod https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/health
Start-Process https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net/portal
```

## Infraestructura declarativa

El repositorio mantiene definiciones Terraform y Bicep en `infra/` como documentación reproducible de la infraestructura. El despliegue final validado se realizó con el script PowerShell porque permite configurar en un único flujo la identidad administrada, Key Vault, variables de entorno y publicación ZIP.

## Compilación de memoria y anexos

```powershell
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

