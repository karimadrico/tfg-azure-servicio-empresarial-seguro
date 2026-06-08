resource "azurerm_service_plan" "plan" {
  name                = "asp-tfg-cloudautomation"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "app-tfg-incidencias-dev"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }

    always_on = true

    app_command_line = "gunicorn --bind=0.0.0.0:8000 --workers=2 app:app"
  }

  app_settings = {
    SCM_DO_BUILD_DURING_DEPLOYMENT = "true"
    STORAGE_MODE                   = "azure"
    AZURE_STORAGE_CONNECTION_STRING = azurerm_storage_account.storage.primary_connection_string
    AZURE_STORAGE_CONTAINER        = azurerm_storage_container.incidencias.name
    AZURE_STORAGE_BLOB             = "incidencias.json"
    KEY_VAULT_URL                  = azurerm_key_vault.kv.vault_uri
    KEY_VAULT_SECRET_NAME          = "api-key"
    API_KEY                        = ""
    WEBSITES_PORT                  = "8000"
  }

  depends_on = [azurerm_storage_container.incidencias]
}
