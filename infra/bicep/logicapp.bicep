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
                servicio_id: {
                  type: 'string'
                }
                activo_id: {
                  type: 'string'
                }
                entorno: {
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
                  servicio_id: '@{coalesce(triggerBody()?[\'servicio_id\'], \'general\')}'
                  activo_id: '@{coalesce(triggerBody()?[\'activo_id\'], \'puesto-usuario\')}'
                  entorno: '@{coalesce(triggerBody()?[\'entorno\'], \'corporativo\')}'
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
            notificar_si_requiere_aprobacion: {
              type: 'If'
              runAfter: {
                crear_solicitud: [
                  'Succeeded'
                ]
              }
              expression: '@equals(body(\'crear_solicitud\')?[\'requiere_aprobacion\'], true)'
              actions: {
                registrar_notificacion_aprobacion: {
                  type: 'Http'
                  inputs: {
                    method: 'POST'
                    uri: '@{concat(parameters(\'apiBaseUrl\'), \'/solicitudes/\', body(\'crear_solicitud\')?[\'id\'], \'/notificar-aprobacion\')}'
                    headers: {
                      'Content-Type': 'application/json'
                      Authorization: '@{concat(\'Bearer \', parameters(\'apiKey\'))}'
                    }
                    body: {
                      canal: 'logic_app'
                      aprobador: '@{body(\'crear_solicitud\')?[\'aprobador\']}'
                    }
                  }
                }
              }
              else: {
                actions: {}
              }
            }
            responder_cliente: {
              type: 'Response'
              runAfter: {
                notificar_si_requiere_aprobacion: [
                  'Succeeded'
                ]
              }
              inputs: {
                statusCode: '@outputs(\'crear_solicitud\')?[\'statusCode\']'
                body: '@body(\'crear_solicitud\')'
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
          runtimeConfiguration: {
            secureData: {
              properties: [
                'inputs'
                'outputs'
              ]
            }
          }
        }
        capturar_error: {
          type: 'Scope'
          runAfter: {
            intentar_crear_solicitud: [
              'Failed'
              'TimedOut'
            ]
          }
          actions: {
            responder_error: {
              type: 'Response'
              inputs: {
                statusCode: 502
                body: {
                  error: 'No se pudo registrar la solicitud en la API.'
                  detalle: '@result(\'intentar_crear_solicitud\')'
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

