
#Creación de un conjunto de escalado de máquinas virtuales de Azure mediante Terraform
#1 Bloques de terraform
terraform {
  #2 Acepta cadena de restricción de versión
  required_version = ">=0.12"
  #3 Administrar las versiones esperadas para cada proveedor que usemos
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

#4 Metaargumento que puede seleccionar una configuración de proveedor alternativa para un recurso:
provider "azurerm" {
  features {}
}
#5 Recursos
#5.1 es un grupo de recursos es un contenedor que almacena los recursos relacionados con una solución de Azure
resource "azurerm_resource_group" "vmss" {
 name     = var.resource_group_name
 location = var.location
 tags     = var.tags
}
#5.2 genera una permutación aleatoria de caracteres alfanuméricos y opcionalmente caracteres especiales
resource "random_string" "fqdn" {
 length  = 6
 special = false
 upper   = false
 number  = false
}

resource "azurerm_virtual_network" "vmss" {
 name                = "vmss-vnet"
 address_space       = ["10.0.0.0/16"]
 location            = var.location
 resource_group_name = azurerm_resource_group.vmss.name
 tags                = var.tags
}

resource "azurerm_subnet" "vmss" {
 name                 = "vmss-subnet"
 resource_group_name  = azurerm_resource_group.vmss.name
 virtual_network_name = azurerm_virtual_network.vmss.name
 address_prefixes       = ["10.0.2.0/24"]
}


#5.5 Administra una dirección IP pública
resource "azurerm_public_ip" "vmss" {
 name                         = "vmss-public-ip"
 location                     = var.location
 resource_group_name          = azurerm_resource_group.vmss.name
 allocation_method            = "Static"
 domain_name_label            = random_string.fqdn.result
 tags                         = var.tags
}
#5.6 Administra un recurso de equilibrador de carga
resource "azurerm_lb" "vmss" {
 name                = "vmss-lb"
 location            = var.location
 resource_group_name = azurerm_resource_group.vmss.name

 frontend_ip_configuration {
   name                 = "PublicIPAddress"
   public_ip_address_id = azurerm_public_ip.vmss.id
 }

 tags = var.tags
}
#5.7 Administra un conjunto de direcciones de back-end del equilibrador de carga
resource "azurerm_lb_backend_address_pool" "bpepool" {
 loadbalancer_id     = azurerm_lb.vmss.id
 name                = "BackEndAddressPool"
}
#5.8 Administra un recurso de sonda LoadBalancer
resource "azurerm_lb_probe" "vmss" {
 resource_group_name = azurerm_resource_group.vmss.name
 loadbalancer_id     = azurerm_lb.vmss.id
 name                = "ssh-running-probe"
 port                = var.application_port
}
#5.9 Administra una regla del equilibrador de carga
resource "azurerm_lb_rule" "lbnatrule" {
   resource_group_name            = azurerm_resource_group.vmss.name
   loadbalancer_id                = azurerm_lb.vmss.id
   name                           = "http"
   protocol                       = "Tcp"
   frontend_port                  = var.application_port
   backend_port                   = var.application_port
   frontend_ip_configuration_name = "PublicIPAddress"
   probe_id                       = azurerm_lb_probe.vmss.id
}


resource "azurerm_public_ip" "jumpbox" {
 name                         = "jumpbox-public-ip"
 location                     = var.location
 resource_group_name          = azurerm_resource_group.vmss.name
 allocation_method            = "Static"
 domain_name_label            = "${random_string.fqdn.result}-ssh"
 tags                         = var.tags
}


#5.13 Grupo de recursos 
resource "azurerm_network_security_group" "vmss" {
  name                = "myTFNSG"
  location            = var.location
  resource_group_name = azurerm_resource_group.vmss.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

    security_rule {
    name                       = "allow-http"
    description                = "allow-http"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

#5.16 conectar el grupo de seguridad en la interfaz de red:
resource "azurerm_network_interface_security_group_association" "vmss" {
    network_interface_id      = azurerm_network_interface.jumpbox.id
    network_security_group_id = azurerm_network_security_group.vmss.id
}
###########################################################################################################################################################################################################################
#5.14 Discos
resource "azurerm_managed_disk" "vmss" {
  name                 = "VM"
  location             = var.location
  resource_group_name  = var.resource_group_name
  storage_account_type = "Standard_LRS"
  create_option        = "Empty"
  disk_size_gb         = "1023"
}


data "template_file" "linux-vm-cloud-init" {
  template = file("azure-user-data.sh")
}


#5.11  Administra una interfaz de red
resource "azurerm_network_interface" "jumpbox" {
 name                = "jumpbox-nic"
 location            = var.location
 resource_group_name = azurerm_resource_group.vmss.name

 ip_configuration {
   name                          = "IPConfiguration"
   subnet_id                     = azurerm_subnet.vmss.id
   private_ip_address_allocation = "dynamic"
   public_ip_address_id          = azurerm_public_ip.jumpbox.id
 }

 tags = var.tags
}
resource "azurerm_virtual_machine" "vmss" {
  name                  = "VMS"
  location              = var.location
  resource_group_name   = var.resource_group_name
  network_interface_ids = [azurerm_network_interface.jumpbox.id]
  vm_size               = "Standard_DC2s_v3"

  storage_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  # Discos de datos opcionales
  storage_data_disk {
    name              = "datadisk_new"
    managed_disk_type = "Standard_LRS"
    create_option     = "Empty"
    lun               = 0
    disk_size_gb      = "1023"
  }

  storage_data_disk {
    name            = "${azurerm_managed_disk.vmss.name}"
    managed_disk_id = "${azurerm_managed_disk.vmss.id}"
    create_option   = "Attach"
    lun             = 1
    disk_size_gb    = "${azurerm_managed_disk.vmss.disk_size_gb}"
  }

  os_profile {
    computer_name  = "hostname"
    admin_username = "testadmin"
    admin_password = "Password1234!"
    custom_data = base64encode(data.template_file.linux-vm-cloud-init.rendered)
    
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  }

#3 Implementación de Runbooks y cuentas de Azure Automation a través de Terraform
resource "azurerm_automation_account" "aa" {
  name                = "AutomationAccount"
  location            = var.location
  resource_group_name = var.resource_group_name

  sku_name = "Basic"

}


