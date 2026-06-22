@description('Region de despliegue')
param location string

@description('URL base de la API desplegada')
param apiBaseUrl string

@description('Clave Bearer para invocar la API')
@secure()
param apiKey string

var logicAppName = 'logic-tfg-aprobaciones-dev'

resource workflow 'Microsoft.Logic/workflows@2019-05-01' = {
  name: logicAppName
  location: location
  tags: {
    Environment: 'Development'
    Project: 'TFG'
    ManagedBy: 'Bicep'
  }
  properties: {
    state: 'Enabled'
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      contentVersion: '1.0.0.0'
      parameters: {
        apiBaseUrl: { type: 'String' }
        apiKey: { type: 'SecureString' }
      }
      triggers: {
        decision_http: {
          type: 'Request'
          kind: 'Http'
          inputs: {
            method: 'POST'
            schema: {
              type: 'object'
              required: [
                'solicitud_id'
                'decision'
                'actor'
              ]
              properties: {
                solicitud_id: { type: 'string' }
                decision: {
                  type: 'string'
                  enum: [
                    'aprobar'
                    'rechazar'
                  ]
                }
                actor: { type: 'string' }
                comentario: { type: 'string' }
              }
            }
          }
          runtimeConfiguration: {
            secureData: {
              properties: [
                'inputs'
                'outputs'
              ]
            }
          }
        }
      }
      actions: { // NOSONAR: responder_decision gestiona Succeeded, Failed y TimedOut sin exponer detalles internos.
        actualizar_aprobacion: {
          type: 'Http'
          inputs: {
            method: 'POST'
            uri: '@{concat(parameters(\'apiBaseUrl\'), \'/solicitudes/\', triggerBody()?[\'solicitud_id\'], \'/aprobacion\')}'
            headers: {
              'Content-Type': 'application/json'
              Authorization: '@{concat(\'Bearer \', parameters(\'apiKey\'))}'
            }
            body: {
              decision: '@{triggerBody()?[\'decision\']}'
              actor: '@{triggerBody()?[\'actor\']}'
              comentario: '@{coalesce(triggerBody()?[\'comentario\'], \'\')}'
            }
          }
          runtimeConfiguration: {
            secureData: {
              properties: [
                'inputs'
                'outputs'
              ]
            }
          }
        }
        responder_decision: { // NOSONAR: Azure Response admite secure inputs, pero rechaza secure outputs en el despliegue.
          type: 'Response'
          runAfter: {
            actualizar_aprobacion: [
              'Succeeded'
              'Failed'
              'TimedOut'
            ]
          }
          inputs: {
            statusCode: '@outputs(\'actualizar_aprobacion\')?[\'statusCode\']'
            body: '@body(\'actualizar_aprobacion\')'
          }
          runtimeConfiguration: {
            secureData: {
              properties: [
                'inputs'
              ]
            }
          }
        }
      }
    }
    parameters: {
      apiBaseUrl: { value: apiBaseUrl }
      apiKey: { value: apiKey }
    }
  }
}

output logicAppName string = workflow.name
