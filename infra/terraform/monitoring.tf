resource "azurerm_application_insights" "app" {
  name                = "appi-tfg-incidencias-dev"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
}
