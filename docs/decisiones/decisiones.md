# Decisiones Técnicas del Proyecto

## 1. Decisión: Uso de Microsoft Azure como Plataforma Cloud

### Contexto
Se necesitaba seleccionar una plataforma cloud que permitiera demostrar una arquitectura empresarial con seguridad integrada.

### Alternativas evaluadas
- **AWS**: amplia, con curva de aprendizaje más alta.
- **Google Cloud**: buena oferta, pero menor integración de seguridad nativa.
- **Microsoft Azure**: seleccionada por su ecosistema y servicios empresariales.

### Justificación
1. **Experiencia previa**: trabajo anterior con Azure en BBVA.
2. **Servicios gestionados**: reduce la carga operativa.
3. **Seguridad integrada**: Key Vault, Entra ID y RBAC.
4. **Plan gratuito para estudiantes**: facilita acceso a recursos reales.
5. **Ecosistema profesional**: alineado con el mercado laboral.

### Decisión final
Microsoft Azure como proveedor cloud principal.

### Impacto en el proyecto
- Arquitectura empresarial más coherente.
- Validación práctica de un entorno real.

---

## 2. Decisión: Python + Flask para la API

### Contexto
Se requería un framework ligero y flexible para el desarrollo rápido de la API.

### Alternativas evaluadas
- **Java (Spring Boot)**: robusto pero con mayor complejidad.
- **Node.js (Express)**: adecuado, pero con menos experiencia previa.
- **Python (Flask)**: elegido por rapidez y simplicidad.

### Justificación
1. **Curva de aprendizaje**: permite iterar con rapidez.
2. **Flexibilidad**: fácil integración con servicios Azure.
3. **Comunidad**: amplio soporte y ejemplos disponibles.
4. **Tiempo de desarrollo**: crítico en el contexto del TFG.
5. **Testing**: compatibilidad con pytest y buenas prácticas.

### Decisión final
Se utiliza Flask para la API REST y Python 3.14 en Azure App Service.

### Impacto en el proyecto
- Código claro y fácil de mantener.
- Despliegue ágil en Azure.

---

## 3. Decisión: Gestión Centralizada de Secretos con Azure Key Vault

### Contexto
Las credenciales no deben almacenarse en el código. Era necesario un enfoque empresarial seguro.

### Alternativas evaluadas
- **Variables de entorno**: insuficiente para un proyecto de nivel empresarial.
- **Archivos .env**: riesgo elevado de exposición.
- **Azure Key Vault**: solución segura y auditada.

### Justificación
1. **Seguridad**: almacenamiento de secretos protegido.
2. **Cumplimiento**: encaja con GDPR y normativas similares.
3. **Auditoría**: registro de accesos y operaciones.
4. **Rotación**: actualización de credenciales sin redeploy.
5. **Integración**: compatibilidad con identidades administradas.

### Decisión final
Azure Key Vault para la gestión de secretos y credenciales.

### Impacto en el proyecto
- Refuerza la madurez de la seguridad.
- Alinea el proyecto con estándares empresariales.

---

## 4. Decisión: Caso de Uso - Gestión de Incidencias Empresariales

### Contexto
Se necesitaba un caso de uso realista y con un alcance adecuado para el TFG.

### Alternativas evaluadas
- Gestión de documentos: demasiado genérico.
- E-commerce: excesivamente complejo.
- Gestión de incidencias: opción equilibrada y representativa.

### Justificación
1. **Realismo**: problema frecuente en empresas.
2. **Alcance**: suficientemente relevante sin ser inabarcable.
3. **Escalabilidad**: permite demostrar la arquitectura.
4. **Automatización**: permite añadir clasificación y triage.
5. **Valor empresarial**: aplicación directa a procesos reales.

### Decisión final
Gestión y automatización de incidencias como caso de negocio.

### Impacto en el proyecto
- Solución práctica y fácilmente evaluable.
- Demuestra análisis de requisitos reales.

---

## 5. Decisión: Metodología Ágil - Scrum con Sprints de 2 Semanas

### Contexto
Se requería una planificación estructurada con entregas periódicas.

### Alternativas evaluadas
- **Waterfall**: demasiado rígido para el entorno del TFG.
- **Kanban**: buena gestión, pero con menor énfasis en hitos.
- **Scrum**: elegido por su estructura de sprints.

### Justificación
1. **Requisito académico**: el plan de proyecto debe incluir sprints.
2. **Validación continua**: facilita revisiones periódicas con el tutor.
3. **Entregas funcionales**: permite mostrar avances claros.
4. **Visibilidad**: seguimiento de tareas y resultados.

### Decisión final
Scrum adaptado con cinco sprints registrados en Zube.
- Sprint 1: 25 Feb - 10 Mar (preparación y base).
- Sprint 2: 11 Mar - 24 Mar (implementación de módulos y dashboard).
- Sprint 3: 25 Mar - 21 Abr (incidencias y despliegue).
- Sprint 4: 22 Abr - 21 May (consolidación y documentación técnica).
- Sprint 5: 22 May - 08 Jul (finalización y defensa).

### Impacto en el proyecto
- Planificación clara y con entregables definidos.
- Mejora la coordinación del trabajo.

---

## 6. Decisión: Herramientas de Gestión - Zube.io para Kanban

### Contexto
Se buscaba una herramienta que facilitara la visualización del progreso.

### Alternativas evaluadas
- **GitHub Issues**: funcional, pero limitado para tablero.
- **Jira**: potente, pero demasiado complejo para el proyecto.
- **Zube.io**: elección por su simplicidad y conexión con GitHub.

### Justificación
1. **Integración**: vincula tareas con repositorio GitHub.
2. **Simplicidad**: interfaz accesible.
3. **Transparencia**: seguimiento claro del progreso.
4. **Comunicación**: facilita mostrar el estado al tribunal.

### Decisión final
Se utiliza Zube.io para la gestión de tareas.

### Impacto en el proyecto
- Más claridad en el seguimiento de las actividades.
- Mejora la presentación del proceso.

---

## 7. Decisión: Despliegue reproducible con Azure CLI y PowerShell

### Contexto
Era necesario un despliegue seguro y repetible hacia Azure. Para la entrega se priorizó un mecanismo local, auditable y verificable.

### Alternativas evaluadas
- **Azure DevOps Pipelines**: separado del repositorio y más complejo.
- **Automatización remota del repositorio**: integración cómoda, pero no fue el camino operativo final.
- **PowerShell + Azure CLI**: reproducible desde el equipo de desarrollo y fácil de demostrar.

### Justificación
1. **Reproducibilidad**: el script ejecuta siempre los mismos pasos.
2. **Seguridad**: integra Key Vault y Managed Identity.
3. **Transparencia**: cada comando puede revisarse y explicarse en defensa.
4. **Viabilidad**: no depende de servicios externos de ejecución.

### Decisión final
PowerShell y Azure CLI para el despliegue operativo final.

### Impacto en el proyecto
- Despliegue reproducible y demostrable.
- Configuración explícita de App Service, Storage, Key Vault y Managed Identity.

---

## 8. Decisión: Documentación en LaTeX + Markdown

### Contexto
La memoria del TFG requiere una estructura formal en PDF y documentación complementaria.

### Alternativas evaluadas
- **Solo Word**: no óptimo para control de versiones.
- **Solo LaTeX**: válido, pero menos práctico para documentación rápida.
- **LaTeX + Markdown**: equilibrio entre formalidad y flexibilidad.

### Justificación
1. **Formato oficial**: LaTeX es compatible con plantillas académicas.
2. **Control de versiones**: texto plano en Git.
3. **Documentación técnica**: Markdown es ágil para avances y especificaciones.
4. **Seguimiento**: los cambios se reflejan claramente en commits.

### Decisión final
Uso combinado de LaTeX para la memoria y Markdown para documentación técnica.

### Impacto en el proyecto
- Combina formalidad académica con rapidez de desarrollo.
- Facilita el control de cambios y la revisión.

---

## 9. Decisión: Componente de IA - Clasificación Automática Simple

### Contexto
El proyecto incluye un componente de IA ligero según la propuesta del TFG.

### Alternativas evaluadas
- **Azure OpenAI**: solución potente, pero excesiva para este alcance.
- **Machine Learning complejo**: riesgo de sobrecarga de implementación.
- **Reglas simples**: opción viable para el alcance actual.

### Justificación
1. **Viabilidad**: puede implementarse dentro del proyecto.
2. **Escalabilidad**: base adecuada para futuras mejoras.
3. **Valor**: añade inteligencia al caso de uso.
4. **Aprendizaje**: introducción práctica a la clasificación.

### Decisión final
Clasificación automática mediante reglas y patrones básicos.

### Impacto en el proyecto
- Añade un componente inteligente sin complicar el alcance.
- Permite futuras mejoras con modelos más avanzados.

---

## 10. Resumen de Decisiones Críticas

- **Cloud**: Azure, elegida por su seguridad y servicios empresariales; aporta una arquitectura de nivel empresarial.
- **Backend**: Flask, elegida por su agilidad y flexibilidad; facilita un prototipado rápido.
- **Seguridad**: Azure Key Vault, para la gestión segura de secretos; aporta un enfoque empresarial sólido.
- **Caso de uso**: Gestión de incidencias, por su realismo y escalabilidad; proporciona una solución práctica.
- **Metodología**: Scrum, para entregas periódicas y validación continua; permite una planificación clara.
- **Tareas**: Zube.io, por su integración con GitHub; mejora la visibilidad del progreso.
- **Despliegue**: PowerShell + Azure CLI, por reproducibilidad y control directo del entorno.
- **Documentación**: LaTeX + Markdown, por formalidad y agilidad; asegura documentación sólida.
- **IA**: Clasificación automática simple, por viabilidad y valor; constituye una base para evolución.

---

## Decisiones cerradas para la entrega

1. **Persistencia**: Azure Blob Storage para solicitudes en formato JSON, con modo local para pruebas.
2. **Observabilidad**: endpoint `/health`, logs de App Service y revisión básica en Azure Portal.
3. **Calidad**: SonarCloud conectado al repositorio y documentado como evidencia externa.
4. **Despliegue final**: PowerShell + Azure CLI como mecanismo operativo validado.
5. **Evolución posterior**: Azure OpenAI, Azure AD, Application Insights, Cosmos DB o Azure SQL quedan como líneas futuras, no como alcance entregado.
