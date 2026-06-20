@description('Región de despliegue')
param location string

@description('Etiquetas de recursos')
param tags object

@secure()
param storageConnectionString string

param keyVaultUri string
@secure()
param applicationInsightsConnectionString string

var webAppName = 'app-tfg-incidencias-dev'
var planName = 'asp-tfg-cloudautomation'

resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: planName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  tags: tags
  properties: {
    reserved: true
  }
}

// La autenticacion funcional se implementa en la API con Bearer token y Key Vault.
resource webApp 'Microsoft.Web/sites@2023-01-01' = { // NOSONAR
  name: webAppName
  location: location
  kind: 'app,linux'
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    clientCertEnabled: true
    clientCertMode: 'Required'
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: true
      ftpsState: 'Disabled'
      appCommandLine: 'gunicorn --bind=0.0.0.0:8000 --workers=2 app:app' // NOSONAR
      appSettings: [
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
        { name: 'WEBSITES_PORT', value: '8000' }
        { name: 'STORAGE_MODE', value: 'azure' }
        { name: 'AZURE_STORAGE_CONNECTION_STRING', value: storageConnectionString }
        { name: 'AZURE_STORAGE_CONTAINER', value: 'incidencias' }
        { name: 'AZURE_STORAGE_BLOB', value: 'incidencias.json' }
        { name: 'KEY_VAULT_URL', value: keyVaultUri }
        { name: 'KEY_VAULT_SECRET_NAME', value: 'api-key' }
        { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: applicationInsightsConnectionString }
      ]
    }
  }
}

resource authSettings 'Microsoft.Web/sites/config@2023-01-01' = {
  parent: webApp
  name: 'authsettingsV2'
  properties: {
    platform: {
      enabled: true
      runtimeVersion: '~1'
    }
    globalValidation: {
      requireAuthentication: true
      unauthenticatedClientAction: 'Return401'
    }
    login: {
      tokenStore: {
        enabled: true
      }
    }
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output principalId string = webApp.identity.principalId

