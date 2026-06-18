@description('Región de despliegue')
param location string

@description('Etiquetas de recursos')
param tags object

var appInsightsName = 'appi-tfg-incidencias-dev'

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}

output connectionString string = appInsights.properties.ConnectionString
output appInsightsName string = appInsights.name
