resource "azurerm_key_vault" "kv" {
  name                = "kv-tfg-enterprise"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = var.tenant_id
  sku_name            = "standard"
}