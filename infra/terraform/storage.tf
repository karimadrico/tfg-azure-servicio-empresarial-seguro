resource "azurerm_storage_account" "storage" {
  name                     = "sttfgincidenciasdev"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_storage_container" "incidencias" {
  name                  = "incidencias"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}
