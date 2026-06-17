variable "location" {
  description = "Región de Azure donde se despliegan los recursos"
  type        = string
  default     = "Sweden Central"
}

variable "tenant_id" {
  description = "Tenant ID de Azure AD (opcional, se obtiene del contexto actual)"
  type        = string
  default     = ""
}

variable "object_id" {
  description = "Object ID del desplegador (opcional)"
  type        = string
  default     = ""
}

variable "api_key" {
  description = "Clave API almacenada en Key Vault"
  type        = string
  sensitive   = true
  default     = "tfg-api-key-ubu-2026"
}
