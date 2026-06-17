@description('Región de despliegue')
param location string

@description('Etiquetas de recursos')
param tags object

@secure()
param storageConnectionString string

param keyVaultUri string
param keyVaultPrincipalId string

var webAppName = 'app-tfg-incidencias-dev'
var planName = 'asp-tfg-cloudautomation'

resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: planName
  location: location
  tags: tags
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  tags: tags
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: true
      appCommandLine: 'gunicorn --bind=0.0.0.0:8000 --workers=2 app:app'
      appSettings: [
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'WEBSITES_PORT', value: '8000' }
        { name: 'STORAGE_MODE', value: 'azure' }
        { name: 'AZURE_STORAGE_CONNECTION_STRING', value: storageConnectionString }
        { name: 'AZURE_STORAGE_CONTAINER', value: 'incidencias' }
        { name: 'AZURE_STORAGE_BLOB', value: 'incidencias.json' }
        { name: 'KEY_VAULT_URL', value: keyVaultUri }
        { name: 'KEY_VAULT_SECRET_NAME', value: 'api-key' }
        { name: 'API_KEY', value: '' }
      ]
    }
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output principalId string = webApp.identity.principalId
