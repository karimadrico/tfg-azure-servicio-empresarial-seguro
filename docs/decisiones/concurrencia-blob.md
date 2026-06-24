# Concurrencia del almacenamiento documental

## Decisión adoptada

El prototipo almacena la colección de solicitudes en un único blob JSON. La API es el único componente que descarga, valida y modifica el documento; el portal y la Logic App siempre acceden a los datos mediante operaciones HTTP de la API.

Este diseño mantiene el mismo formato en ejecución local y en Azure, reduce el número de componentes y facilita inspeccionar el resultado durante la validación. Su alcance es una demostración de bajo volumen y no una plataforma ITSM destinada a carga concurrente de producción.

## Comportamiento concurrente

La implementación sigue una secuencia de lectura, modificación en memoria y sobrescritura. No utiliza ETag, condición `If-Match`, transacción ni bloqueo distribuido. Si dos procesos leen la misma versión N, el primero puede guardar N+A y el segundo N+B; la segunda escritura puede eliminar el cambio de la primera. Los dos procesos también podrían calcular el mismo identificador secuencial `SOL-XXX`.

Un bloqueo en memoria únicamente coordinaría un proceso. No resolvería el conflicto entre varios workers de Gunicorn o entre varias instancias de App Service. La API centraliza las reglas de escritura, pero esa frontera no proporciona por sí sola exclusión mutua.

## Evolución del modelo

La mejora mínima consiste en recuperar el ETag del blob, escribir con `If-Match` y reintentar la operación cuando la versión almacenada haya cambiado. Para un volumen mayor se separarían las solicitudes en objetos independientes o se utilizaría Azure Table Storage, Cosmos DB o Azure SQL, en función de las consultas y garantías transaccionales requeridas.

La decisión permite demostrar persistencia cloud y trazabilidad con una implementación acotada, a la vez que identifica de forma explícita el riesgo de última escritura ganadora y el límite de escalabilidad del prototipo.
