# Problema empresarial

Las áreas de TI reciben solicitudes internas por canales muy distintos: correo electrónico, chats, hojas de cálculo, formularios no conectados o conversaciones informales. En ese contexto resulta difícil mantener una visión única de qué se ha pedido, quién debe aprobarlo, qué prioridad tiene, qué servicio está afectado y qué plazo de resolución debería aplicarse.

## Problemas observados

- Falta de trazabilidad entre solicitud, responsable, estado e historial.
- Priorización manual poco homogénea entre accesos, incidencias y cambios de configuración.
- Gestión dispersa de credenciales y tokens de integración.
- Ausencia de métricas operativas para revisar carga, SLA, escalados y satisfacción.
- Dificultad para integrar formularios o sistemas externos sin duplicar reglas de negocio.
- Riesgo de que el almacenamiento inicial no escale bien si todas las solicitudes se concentran en un único documento.

## Solución planteada

El TFG desarrolla una plataforma cloud de solicitudes TI desplegada en Microsoft Azure. La solución centraliza el proceso en una API Flask alojada en App Service, utiliza Azure Cosmos DB como persistencia documental, protege el token de evaluación en Key Vault, incorpora Managed Identity y añade una Logic App como canal de entrada desde sistemas externos.

La aplicación permite registrar solicitudes, clasificarlas con reglas explicables, calcular prioridad e impacto, gestionar aprobaciones, revisar SLA, escalar casos, cerrar solicitudes, recoger valoración y exportar información operativa. El centro operativo resume carga de trabajo, alertas y satisfacción para que el producto no quede limitado a un formulario de tickets.

## Alcance

El prototipo no sustituye a una plataforma ITSM comercial. Su finalidad es demostrar análisis, diseño, implementación, despliegue, seguridad, automatización, persistencia cloud, calidad de código y validación funcional dentro del alcance de un Trabajo Fin de Grado.
