# Infraestructura Terraform

## Recursos provisionados

| Recurso | Nombre | Descripción |
|---------|--------|-------------|
| Resource Group | `rg-tfg-cloudautomation-dev` | Contenedor de recursos |
| App Service Plan | `asp-tfg-cloudautomation` | Plan Linux B1 |
| Web App | `app-tfg-incidencias-dev` | API Flask con Managed Identity |
| Storage Account | `tfgstorage001` | Persistencia de incidencias |
| Blob Container | `incidencias` | Contenedor privado |
| Key Vault | `kv-tfg-enterprise` | Secreto `api-key` |

## Despliegue

```bash
cd infra/terraform
terraform init
terraform plan -var="api_key=<tu-clave>"
terraform apply -var="api_key=<tu-clave>"
```

## Outputs

- `webapp_url`: URL pública de la API
- `key_vault_uri`: URI del Key Vault
- `storage_account_name`: nombre del Storage Account
