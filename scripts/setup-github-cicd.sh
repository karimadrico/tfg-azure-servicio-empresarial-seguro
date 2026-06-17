#!/usr/bin/env bash
# Configuracion de CI/CD con GitHub Actions
# Repositorio: https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro

set -euo pipefail

SUBSCRIPTION_ID="a79fdf71-ae1e-4475-bebd-4a60a662e0ee"
SP_NAME="sp-tfg-github-actions"
RESOURCE_GROUP="rg-tfg-cloudautomation-dev"
GITHUB_REPO="https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro"

if ! command -v az >/dev/null 2>&1; then
  echo "Azure CLI no esta disponible."
  exit 1
fi

az account show >/dev/null 2>&1 || az login

echo "Configurando Service Principal para GitHub Actions"
echo "Repositorio: $GITHUB_REPO"
echo "Suscripcion: Azure for Students ($SUBSCRIPTION_ID)"
echo "Resource Group: $RESOURCE_GROUP"
echo ""

CREDS=$(az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role contributor \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP" \
  --sdk-auth)

echo ""
echo "================================================"
echo " Secretos para GitHub Actions"
echo " Repositorio: karimadrico/tfg-azure-servicio-empresarial-seguro"
echo " Settings > Secrets and variables > Actions"
echo "================================================"
echo ""
echo "Nombre: AZURE_CREDENTIALS"
echo "Valor:"
echo "$CREDS"
echo ""
echo "Nombre: TFG_API_KEY"
echo "Valor: tfg-api-key-ubu-2026"
echo ""
echo "Despues de guardar los secretos, hago push a main"
echo "y el workflow .github/workflows/deploy.yml se ejecuta solo."
echo "================================================"
