# Decisiones técnicas

Este documento resume decisiones que pueden comprobarse en el código, los scripts o el despliegue. Las alternativas no se presentan como inferiores en general; se explica por qué no encajaban igual de bien en el alcance del prototipo.

## Microsoft Azure

La propuesta del TFG requería desplegar una solución empresarial segura en Microsoft Azure y la suscripción Azure for Students permitía trabajar con recursos reales. AWS y Google Cloud habrían ofrecido servicios equivalentes, pero cambiar de proveedor no aportaba valor al objetivo académico.

Consecuencia: toda la arquitectura utiliza servicios gestionados de Azure y una única región, Sweden Central.

## Flask para la API

La aplicación necesita pocas rutas, validación JSON y una interfaz web pequeña. Flask permite mantener esas responsabilidades visibles y no obliga a incorporar un ORM o un panel de administración. Django sería más adecuado si el sistema tuviera un dominio relacional amplio, usuarios propios y administración de datos.

Consecuencia: la estructura se reparte entre `app.py`, `classifier.py`, `storage.py` y `config.py`.

## Blob Storage para las solicitudes

Cada solicitud se guarda como un documento JSON y el prototipo no necesita relaciones ni transacciones entre tablas. SQLite habría simplificado el modo local, mientras que Azure SQL habría facilitado consultas complejas. Blob Storage encaja mejor con el objetivo de probar persistencia gestionada en Azure con un volumen reducido.

Consecuencia: `storage.py` ofrece modo local y modo Azure, pero la evolución hacia búsquedas avanzadas requeriría otra tecnología de datos.

## Key Vault y Managed Identity

La clave Bearer de consulta no debe estar en el repositorio. Key Vault la centraliza y Managed Identity permite que App Service la recupere sin guardar otra credencial de Azure en la aplicación.

Consecuencia: el despliegue asigna identidad a App Service, concede el rol mínimo necesario y configura una referencia al secreto.

## Clasificación basada en reglas

No existía un conjunto de solicitudes históricas etiquetadas con el que entrenar y evaluar un modelo. El clasificador utiliza palabras clave, puntuaciones y reglas de prioridad; por eso cada resultado puede reproducirse y explicarse. Un servicio de lenguaje podría evaluarse en el futuro si se dispone de datos y de una métrica de comparación.

Consecuencia: el componente aporta análisis automático, pero no aprende de nuevas solicitudes.

## Despliegue con PowerShell y Azure CLI

Durante la planificación se exploró GitHub Actions. La entrega final utiliza `deploy-azure.ps1` y `verify-azure.ps1` porque son los mecanismos que se ejecutaron contra la suscripción y dejan visibles los comandos de configuración y comprobación.

Consecuencia: el despliegue es repetible desde el entorno local, pero no existe promoción automática entre varios entornos.

## Terraform y Bicep

Ambos directorios describen la infraestructura de forma declarativa. No se afirma que fueran el mecanismo de publicación final: cumplen una función documental y permiten comparar dos formas de infraestructura como código con el script operativo.

Consecuencia: cualquier evolución deberá elegir una única fuente de verdad antes de automatizar aprovisionamiento completo.

## Logic App como canal externo

La Logic App recibe una petición HTTP y llama a la misma operación `POST /solicitudes` que utiliza el portal. La validación, clasificación y persistencia permanecen en la API.

Consecuencia: pueden añadirse canales empresariales sin copiar reglas de negocio en cada integración.

## Zube para seguimiento

Zube se utilizó desde el inicio y conserva cinco sprints y sus tarjetas. Cambiar a Azure Boards o Jira al final habría perdido continuidad. Los puntos de historia no se utilizaron; el Anexo A estima el esfuerzo mediante horas.

Consecuencia: las desviaciones de fechas y las tarjetas retiradas se documentan tal como aparecen en el historial.

## SonarCloud y pruebas

SonarCloud aporta una revisión externa del repositorio sin mantener una instancia propia de SonarQube. Las catorce pruebas automáticas verifican el comportamiento funcional, mientras que SonarCloud revisa seguridad, fiabilidad, mantenibilidad y duplicación.

Consecuencia: ninguna de las dos herramientas sustituye a la otra y ambas forman parte de la evidencia de calidad.

## Application Insights y Azure Monitor

El endpoint `/metricas` muestra agregados del proceso y Application Insights recoge telemetría del servicio. Se mantienen separados porque responden a preguntas distintas: qué solicitudes existen y cómo se comporta técnicamente la aplicación.

Consecuencia: la observabilidad es suficiente para una demostración, aunque faltan alertas y objetivos de nivel de servicio propios de producción.
