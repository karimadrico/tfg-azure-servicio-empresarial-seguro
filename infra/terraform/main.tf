resource "azurerm_resource_group" "main" {
  name     = "rg-tfg-cloudautomation-dev"
  location = var.location

  tags = {
    Environment = "Development"
    Project     = "TFG"
    ManagedBy   = "Terraform"
  }
}

data "azurerm_client_config" "current" {}
