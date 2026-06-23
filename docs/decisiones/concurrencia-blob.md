# Concurrencia del almacenamiento documental

## Situación actual

El prototipo almacena todas las solicitudes en un único blob JSON. La API descarga la colección, modifica una copia en memoria y vuelve a subir el documento completo con sobrescritura. Portal y Logic App nunca acceden directamente al blob.

Esta solución reduce componentes, mantiene el mismo formato en local y Azure y facilita inspeccionar los datos durante una demostración. Su alcance es un prototipo de bajo volumen, no una plataforma ITSM de producción.

## Riesgo

No existe control optimista mediante ETag, condición `If-Match`, transacción ni bloqueo distribuido. Si dos procesos leen la misma versión:

1. A y B descargan la colección N.
2. A incorpora su cambio y guarda N+A.
3. B incorpora otro cambio sobre su copia antigua y guarda N+B.
4. La escritura de B puede eliminar el cambio de A.

También podrían generarse identificadores iguales porque ambos procesos calculan el siguiente `SOL-XXX` sobre la misma colección. Un bloqueo local no es suficiente con varios workers o varias instancias.

## Respuesta preparada para la defensa

> Elegí un único blob JSON porque el objetivo era validar el flujo cloud con poco volumen, un formato inspeccionable y el mismo comportamiento local y remoto. La API centraliza todas las escrituras, pero eso no elimina la concurrencia entre workers. Actualmente se aplica última escritura gana y existe riesgo de pérdida de actualización. Para producción usaría ETag e `If-Match` con reintentos como mejora mínima; si aumenta el volumen, separaría documentos o migraría a Table Storage, Cosmos DB o Azure SQL según las consultas y garantías transaccionales necesarias.

## Evolución propuesta

- Corto plazo: escritura condicional con ETag, reintentos y prueba de conflicto.
- Medio plazo: un objeto por solicitud y generación de identificadores no secuenciales.
- Producción: almacén con concurrencia y consultas nativas, índice por estado y servicio, control de acceso por identidad y política de retención.

