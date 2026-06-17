#!/usr/bin/env bash
# Script de despliegue de la API en Azure App Service
# Proyecto: TFG - Universidad de Burgos
# Repositorio: https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Recursos desplegados en Azure for Students (Universidad de Burgos)
RESOURCE_GROUP="rg-tfg-cloudautomation-dev"
WEBAPP_NAME="app-tfg-incidencias-dev"
PLAN_NAME="ASP-rgtfgcloudautomationdev-b089"
LOCATION="swedencentral"
API_KEY="${API_KEY:-tfg-api-key-ubu-2026}"

echo "=== Despliegue API TFG en Azure ==="
echo "Suscripcion:  Azure for Students"
echo "Resource Group: $RESOURCE_GROUP"
echo "App Service:    $WEBAPP_NAME"
echo "Region:         $LOCATION"
echo ""

if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLI no esta disponible. Lo instale desde el instalador incluido en el repositorio (AzureCLI.msi)."
  exit 1
fi

echo "[1/4] Comprobando sesion en Azure..."
az account show >/dev/null 2>&1 || az login

STORAGE_ACCOUNT="sttfgincidenciasdev"
KEY_VAULT_NAME="kv-tfg-incidencias-dev"

echo "[2/6] Obteniendo configuracion de Storage y Key Vault..."
STORAGE_CONN=$(az storage account show-connection-string \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --query connectionString -o tsv)
KV_URL=$(az keyvault show \
  --name "$KEY_VAULT_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query properties.vaultUri -o tsv)

echo "[3/6] Habilitando Managed Identity y acceso a Key Vault..."
PRINCIPAL_ID=$(az webapp identity assign \
  --name "$WEBAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --query principalId -o tsv)

az keyvault set-policy \
  --name "$KEY_VAULT_NAME" \
  --object-id "$PRINCIPAL_ID" \
  --secret-permissions get list \
  --output none

az keyvault secret set \
  --vault-name "$KEY_VAULT_NAME" \
  --name api-key \
  --value "$API_KEY" \
  --output none

echo "[4/6] Configurando variables de entorno en App Service..."
az webapp config appsettings set \
  --name "$WEBAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --settings \
    STORAGE_MODE=azure \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_CONN" \
    AZURE_STORAGE_CONTAINER=incidencias \
    AZURE_STORAGE_BLOB=incidencias.json \
    KEY_VAULT_URL="$KV_URL" \
    KEY_VAULT_SECRET_NAME=api-key \
    API_KEY= \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    WEBSITES_PORT=8000 \
  --output none

az webapp config set \
  --name "$WEBAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --startup-file "gunicorn --bind=0.0.0.0:8000 --workers=2 app:app" \
  --output none

echo "[5/6] Empaquetando codigo de src/..."
TMP_ZIP="/tmp/tfg-api-deploy.zip"
rm -f "$TMP_ZIP"
(cd "$REPO_ROOT/src" && powershell.exe -Command "Compress-Archive -Path * -DestinationPath '$TMP_ZIP' -Force")

echo "[6/6] Publicando en App Service..."
az webapp deployment source config-zip \
  --name "$WEBAPP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --src "$TMP_ZIP" \
  --output none

URL="https://${WEBAPP_NAME}.azurewebsites.net"
echo ""
echo "Despliegue finalizado."
echo "URL:     $URL"
echo "API Key: $API_KEY"
echo ""
echo "Comprobacion:"
echo "curl $URL/"
echo ""
echo "curl -X POST $URL/incidencias \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Authorization: Bearer $API_KEY' \\"
echo "  -d '{\"titulo\":\"Prueba Azure\",\"descripcion\":\"Incidencia registrada desde el despliegue en App Service\",\"reportado_por\":\"karima@ubu.es\"}'"
