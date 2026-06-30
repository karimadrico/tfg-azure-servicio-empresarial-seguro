# Evolución de la persistencia documental

La primera versión cloud del prototipo almacenaba la colección de solicitudes en un único blob JSON. La API era el único componente que descargaba, validaba y modificaba el documento; el portal y la Logic App siempre accedían a los datos mediante operaciones HTTP de la API.

Ese diseño era suficiente para demostrar persistencia gestionada con bajo volumen, pero tenía un límite claro: si dos procesos leían la misma versión del blob y guardaban cambios después, la última escritura podía sobrescribir la anterior. Azure Blob Storage permite mitigar este problema con ETag y escrituras condicionales `If-Match`, pero el modelo seguía concentrando toda la colección en un único objeto.

La rama de evolución de persistencia migra las solicitudes a Azure Cosmos DB. Cada solicitud se conserva como documento JSON independiente en la base de datos `tfg-solicitudes` y el contenedor `solicitudes`, manteniendo la compatibilidad conceptual con el modelo semiestructurado y reduciendo el acoplamiento del blob único.

La API sigue siendo la frontera de acceso: valida, clasifica, calcula SLA, actualiza historial y persiste. Ni el portal ni la Logic App acceden directamente a Cosmos DB. Esta decisión mantiene las reglas de negocio centralizadas y facilita defender la evolución desde una persistencia sencilla hacia una base documental gestionada.
