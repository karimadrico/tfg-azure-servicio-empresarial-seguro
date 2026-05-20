variable "resource_group_name" {
   description = "Nombre del grupo de recursos"
   default     = "TFGkarima"
}

variable "location" {
   default = "eastus2"
   description = "Localización"
}

variable "tags" {
   description = "Map of the tags to use for the resources that are deployed"
   type        = map(string)
   default = {
      environment = "codelab"
   }
}

variable "application_port" {
   description = "Port that you want to expose to the external load balancer"
   default     = 80
}

variable "admin_user" {
   description = "User name to use as the admin account on the VMs that will be part of the VM scale set"
   default     = "karima"
}

variable "admin_password" {
   default     = "Password1234!"
}

variable "prefix" {
   type        = string
   default     = "azterraform"
}

variable "automation_account_name" {
   description = "Name of the resource group in which the resources will be created"
   default     = "AutomationAccount"
}