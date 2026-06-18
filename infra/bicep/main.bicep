@description('Región de despliegue')
param location string = 'swedencentral'

@description('Clave API almacenada en Key Vault')
@secure()
param apiKey string

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

module monitoring 'monitoring.bicep' = {
  name: 'monitoringDeployment'
  params: {
    location: location
    tags: tags
  }
}

module appservice 'appservice.bicep' = {
  name: 'appserviceDeployment'
  params: {
    location: location
    tags: tags
    storageConnectionString: storage.outputs.connectionString
    keyVaultUri: keyvault.outputs.vaultUri
    applicationInsightsConnectionString: monitoring.outputs.connectionString
  }
}

output webAppUrl string = appservice.outputs.webAppUrl
output keyVaultUri string = keyvault.outputs.vaultUri
output storageAccountName string = storage.outputs.storageAccountName
output applicationInsightsName string = monitoring.outputs.appInsightsName
