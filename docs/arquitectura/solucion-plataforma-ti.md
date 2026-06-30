# Arquitectura de la plataforma TI

Este documento resume la solución software entregada: una plataforma cloud para automatizar solicitudes internas de TI sobre Microsoft Azure. El objetivo es que una petición pueda entrar desde el portal web o desde un sistema externo, pasar por las mismas reglas de validación y quedar persistida en Cosmos DB con trazabilidad.

## Proceso empresarial cubierto

| Tipo de solicitud | Ejemplos | Tratamiento aplicado |
|-------------------|----------|----------------------|
| Acceso | VPN, permisos, cuentas | Validación de solicitante, impacto y posible aprobación. |
| Configuración | Cambio de parámetros o entorno | Revisión del servicio afectado y responsable técnico. |
| Soporte | Consulta o petición operativa | Clasificación, responsable y SLA según prioridad. |
| Incidencia | Fallo operativo o interrupción | Priorización, alerta de SLA y seguimiento en centro operativo. |

## Flujo funcional

| Paso | Componente | Resultado |
|------|------------|-----------|
| 1 | Portal web o Logic App | Entrada de la solicitud desde usuario o sistema externo. |
| 2 | API Flask en App Service | Validación de campos, catálogo y token cuando procede. |
| 3 | Reglas de negocio | Cálculo de tipo, prioridad, impacto, SLA, responsable y aprobación. |
| 4 | Azure Cosmos DB | Persistencia de la solicitud como documento JSON independiente. |
| 5 | Centro operativo | Consulta de bandeja, alertas, métricas, escalado, cierre y valoración. |
| 6 | SonarCloud, Zube y GitHub | Evidencias de calidad, planificación y trazabilidad del desarrollo. |

## Automatización con Logic App

La Logic App `logic-tfg-solicitudes-dev` representa el canal de integración con otros sistemas empresariales. Recibe una petición HTTP, construye el cuerpo esperado por la API y llama a `POST /solicitudes` usando el token configurado durante el despliegue. La Logic App no escribe en Cosmos DB ni aplica reglas propias; esa responsabilidad permanece centralizada en la API.

## Clasificación y reglas

El componente de clasificación es ligero y explicable. No depende de un servicio externo de IA ni de datos de entrenamiento. Aplica reglas deterministas para estimar tipo, categoría, prioridad, recomendación y nivel de confianza, lo que permite justificar cada resultado durante la defensa y cubrirlo con pruebas automáticas.

## Seguridad y datos

- Las operaciones internas usan token Bearer.
- El secreto `api-key` se almacena en Azure Key Vault.
- App Service usa Managed Identity para acceder a Key Vault.
- Cosmos DB conserva cada solicitud como documento independiente.
- El portal y la Logic App acceden siempre mediante la API, nunca directamente a la base de datos.
- Las evidencias no muestran secretos, firmas `sig` ni cadenas de conexión.

## Validación

La solución se valida con 27 pruebas automáticas, verificación real contra Azure, Quality Gate aprobado en SonarCloud y capturas de Azure Portal, Zube, GitHub, Logic App, Cosmos DB y el portal desplegado.
