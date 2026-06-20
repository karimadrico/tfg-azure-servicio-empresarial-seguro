@description('Region de despliegue')
param location string

@description('Etiquetas de recursos')
param tags object = {
  Environment: 'Development'
  Project: 'TFG'
  ManagedBy: 'Bicep'
}

@description('URL base de la API desplegada en App Service')
param apiBaseUrl string

@description('Clave Bearer para invocar la API')
@secure()
param apiKey string

var logicAppName = 'logic-tfg-solicitudes-dev'

resource workflow 'Microsoft.Logic/workflows@2019-05-01' = {
  name: logicAppName
  location: location
  tags: tags
  properties: {
    state: 'Enabled'
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      contentVersion: '1.0.0.0'
      parameters: {
        apiBaseUrl: {
          type: 'String'
        }
        apiKey: {
          type: 'SecureString'
        }
      }
      triggers: {
        solicitud_http: {
          type: 'Request'
          kind: 'Http'
          inputs: {
            method: 'POST'
            schema: {
              type: 'object'
              required: [
                'titulo'
                'descripcion'
                'reportado_por'
              ]
              properties: {
                tipo_solicitud: {
                  type: 'string'
                }
                titulo: {
                  type: 'string'
                }
                descripcion: {
                  type: 'string'
                }
                reportado_por: {
                  type: 'string'
                }
                prioridad: {
                  type: 'string'
                }
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
      actions: {
        intentar_crear_solicitud: {
          type: 'Scope'
          actions: {
            crear_solicitud: {
              type: 'Http'
              inputs: {
                method: 'POST'
                uri: '@{concat(parameters(\'apiBaseUrl\'), \'/solicitudes\')}'
                headers: {
                  'Content-Type': 'application/json'
                  Authorization: '@{concat(\'Bearer \', parameters(\'apiKey\'))}'
                }
                body: {
                  tipo_solicitud: '@{coalesce(triggerBody()?[\'tipo_solicitud\'], \'incidencia\')}'
                  titulo: '@{triggerBody()?[\'titulo\']}'
                  descripcion: '@{triggerBody()?[\'descripcion\']}'
                  reportado_por: '@{triggerBody()?[\'reportado_por\']}'
                  prioridad: '@{triggerBody()?[\'prioridad\']}'
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
            responder_cliente: {
              type: 'Response'
              runAfter: {
                crear_solicitud: [
                  'Succeeded'
                ]
              }
              inputs: {
                statusCode: '@outputs(\'crear_solicitud\')?[\'statusCode\']'
                body: '@body(\'crear_solicitud\')'
              }
            }
          }
        }
        responder_error: {
          type: 'Response'
          runAfter: {
            intentar_crear_solicitud: [
              'Failed'
              'TimedOut'
            ]
          }
          inputs: {
            statusCode: 502
            body: {
              error: 'No se pudo registrar la solicitud en la API.'
              detalle: '@result(\'intentar_crear_solicitud\')'
            }
          }
        }
      }
    }
    parameters: {
      apiBaseUrl: {
        value: apiBaseUrl
      }
      apiKey: {
        value: apiKey
      }
    }
  }
}

output logicAppName string = workflow.name

