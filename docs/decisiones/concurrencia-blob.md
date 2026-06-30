# Decisión de persistencia y concurrencia

## Situación inicial

La primera versión cloud utilizó Azure Blob Storage con una colección JSON única. Era una solución sencilla para demostrar persistencia gestionada, inspeccionar el contenido y mantener el mismo formato que las pruebas locales.

## Limitación detectada

El modelo de blob único concentraba todas las solicitudes en un solo objeto. Si dos operaciones leían la misma versión y escribían después, la última escritura podía sobrescribir la anterior. Blob Storage permite controles con ETag y escrituras condicionales, pero el diseño seguía obligando a leer y guardar la colección completa.

## Decisión final

La persistencia final se migró a Azure Cosmos DB. Cada solicitud se almacena como documento JSON independiente en la base de datos `tfg-solicitudes` y el contenedor `solicitudes`, con partición `/tipo_solicitud`.

Esta decisión mantiene el modelo documental del proyecto y mejora la separación de registros. La API continúa siendo la única frontera de acceso: valida, clasifica, calcula SLA, actualiza historial y persiste. El portal y la Logic App no acceden directamente a Cosmos DB.

## Alcance

Cosmos DB resuelve la principal limitación del blob único para el prototipo entregado, pero una implantación productiva debería añadir políticas más completas de concurrencia optimista, auditoría, retención, copias, identidad individual y autorización por roles.
