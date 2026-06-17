@description('Región de despliegue')
param location string = 'swedencentral'

@description('Clave API almacenada en Key Vault')
@secure()
param apiKey string

var resourceGroupName = 'rg-tfg-cloudautomation-dev'
var tags = {
  Environment: 'Development'
  Project: 'TFG'
  ManagedBy: 'Bicep'
}

module storage 'storage.bicep' = {
  name: 'storageDeployment'
  params: {
    location: location
    tags: tags
  }
}

module keyvault 'keyvault.bicep' = {
  name: 'keyvaultDeployment'
  params: {
    location: location
    tags: tags
    apiKey: apiKey
  }
}

module appservice 'appservice.bicep' = {
  name: 'appserviceDeployment'
  params: {
    location: location
    tags: tags
    storageConnectionString: storage.outputs.connectionString
    keyVaultUri: keyvault.outputs.vaultUri
    keyVaultPrincipalId: keyvault.outputs.appPrincipalId
  }
}

output webAppUrl string = appservice.outputs.webAppUrl
output keyVaultUri string = keyvault.outputs.vaultUri
output storageAccountName string = storage.outputs.storageAccountName
output logicAppDeployHint string = 'Importar logicapp/workflow.json como logic-tfg-solicitudes-dev'
