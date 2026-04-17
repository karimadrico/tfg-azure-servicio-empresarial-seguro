# Sprint 1 - Preparación y Base

Período: 25 de febrero - 10 de marzo de 2026

Estado: Completado

Propiedad: Karima Drafli Rico

---

## 1. Objetivos del Sprint

- Definir el proceso empresarial a automatizar.
- Configurar infraestructura básica en Azure.
- Estructurar el repositorio según los estándares de la Universidad.
- Establecer un pipeline CI/CD inicial.
- Diseñar la arquitectura general del sistema.
- Configurar monitorización y calidad de código.

---

## 2. Historias de Usuario Planificadas

### HU-01: Definir proceso empresarial a automatizar
Estado: Completado

Descripción: Analizar y documentar el problema empresarial, casos de uso y requisitos.

Tareas realizadas:
- Documentar el problema: “Gestión manual de incidencias es ineficiente”.
- Definir los casos de uso principales.
- Especificar los requisitos funcionales iniciales.
- Crear el documento de análisis.

Resultado: Documento “Análisis del Proceso Empresarial” en `docs/analisis/`.

Puntos: 8

---

### HU-02: Configurar cuenta de Azure Students
Estado: Completado

Descripción: Obtener acceso a Azure con créditos educativos y crear los recursos iniciales.

Tareas realizadas:
- Crear suscripción Azure con email de estudiante.
- Obtener los créditos educativos disponibles.
- Crear el grupo de recursos `tfg-empresa-rg`.
- Documentar los límites y cuotas del entorno.
- Configurar alertas de gasto.

Resultado: Suscripción activa y grupo de recursos configurado.

Puntos: 5

---

### HU-03: Estructurar el repositorio
Estado: Completado

Descripción: Organizar el repositorio para documentación, código y pruebas.

Tareas realizadas:
- Crear estructura `/memoria` con plantilla UBU en LaTeX.
- Crear carpeta `/docs` para documentación técnica en Markdown.
- Crear `/src/api` para el código Python.
- Crear `/tests` para pruebas.
- Crear `/diagramas` para la documentación de arquitectura.
- Crear un `.gitignore` adecuado.
- Añadir el archivo `README.md` principal.

Resultado: Estructura del repositorio definida y versionada en Git.

Puntos: 5

---

### HU-04: Configurar CI/CD básico
Estado: En progreso (integración con Azure pendiente en Sprint 2)

Descripción: Establecer un pipeline básico en GitHub Actions para validar el código.

Tareas realizadas:
- Crear workflow de validación básica.
- Configurar linting Python con `flake8`.
- Configurar pruebas Python con `pytest`.

Resultado: `.github/workflows/` contiene el pipeline de validación inicial.

Puntos: 8

---

### HU-05: Diseñar arquitectura general
Estado: Completado

Descripción: Definir el modelo de componentes y el flujo de datos del sistema.

Tareas realizadas:
- Diseñar el diagrama de componentes con servicios de Azure.
- Documentar el flujo de datos.
- Justificar la selección de servicios de Azure.
- Crear el diagrama en formato PNG.
- Documentar la arquitectura en `docs/arquitectura/arquitectura.md`.

Resultado: Diagrama y documentación de arquitectura generados.

Puntos: 8

---

### HU-06: Configurar gestor de calidad
Estado: Completado

Descripción: Integrar SonarQube para el análisis de calidad del código.

Tareas realizadas:
- Crear cuenta en SonarCloud.
- Configurar el proyecto `tfg-azure-servicio-empresarial-seguro`.
- Integrar SonarCloud con GitHub Actions.
- Establecer gates de calidad.
- Documentar la configuración en `docs/calidad/`.

Resultado: Dashboard de calidad disponible y conectado al repositorio.

Puntos: 5

---

## 3. Métricas del Sprint

Velocidad:
- Puntos planeados: 39.
- Puntos completados: 36.
- Puntos pospuestos: 3 (HU-04 parcial trasladado a Sprint 2).
- Tasa de completitud: 92%.

Calidad:
- Commits realizados: 8.
- Builds en rama principal: 8/8.
- Coverage: no aplica (sin código aún definitivo).
- Issues críticos en SonarQube: 0.

Cumplimiento:
- Sprint completado a tiempo: Sí.
- Reuniones con tutor: 2.
- Documentación completada: 95%.
- Repositorio actualizado con múltiples commits.

---

## 4. Actividades Realizadas

### Semana 1 (25 Feb - 3 Mar)
- Obtener los créditos de Azure.
- Crear los recursos iniciales en Azure: App Service, Storage y Resource Group.
- Configurar el repositorio con la plantilla oficial UBU en LaTeX.
- Realizar la primera reunión con el tutor.

Commits relevantes:
- 25 Feb: “init: estructura inicial del TFG”.
- 26 Feb: “docs: plantilla LaTeX oficial UBU”.
- 27 Feb: “docs: análisis del problema empresarial”.
- 01 Mar: “azure: crear recursos (App Service, Storage)”.

### Semana 2 (4 Mar - 10 Mar)
- Diseñar la arquitectura del sistema.
- Documentar decisiones técnicas.
- Configurar SonarQube.
- Generar el diagrama de componentes.
- Reunión con el tutor para validar el enfoque.

Commits relevantes:
- 04 Mar: “docs: arquitectura del sistema”.
- 05 Mar: “docs: decisiones técnicas”.
- 07 Mar: “ci: configurar GitHub Actions básico”.
- 09 Mar: “docs: especificación API”.

---

## 5. Problemas Encontrados y Soluciones

Problema 1: Acceso a Azure Key Vault.
Descripción: No se podían crear secretos debido a permisos RBAC.
Solución: Esperar la propagación de los cambios de roles en Azure Active Directory.
Impacto: mínimo.

Problema 2: Alcance inicial demasiado amplio.
Descripción: La propuesta del caso de uso se percibía como genérica.
Solución: Enfocar el proyecto en “Gestión de Incidencias Empresariales”.
Impacto: positivo, el proyecto se volvió más concreto.

Problema 3: Incidencia personal en la semana del 10-17 de marzo.
Descripción: pérdida de mascota y afectación emocional.
Solución: ajustar el ritmo de trabajo y usar una semana de amortiguación.
Impacto: se requiere acelerar Sprint 2 para mantener el cronograma.

---

## 6. Retroalimentación del Tutor

Reunión 1 (25 Feb):
La propuesta es interesante. Se debe concretar el proceso exacto y validar con datos de la empresa.

Reunión 2 (10 Mar):
El enfoque en incidencias es adecuado. La arquitectura tiene un planteamiento profesional. Se requiere un API funcional básico en Sprint 2.

---

## 7. Planes para Sprint 2

Duración: 11 Mar - 24 Mar.

Objetivo principal: obtener un prototipo funcional desplegado en Azure.

Historias planeadas:
- HU-07: Crear Azure Key Vault y gestionar secretos.
- HU-08: Integrar Key Vault con App Service.
- HU-09: Crear la API Python inicial.
- HU-10: Configurar CI/CD con GitHub Actions hacia Azure.
- HU-11: Implementar el sistema de incidencias con persistencia.
- HU-12: Integrar la clasificación automática básica.

Entregables esperados:
- API REST desplegada en Azure con URL pública.
- Endpoints funcionales para crear y consultar incidencias.
- Gestión segura de secretos con Key Vault.
- Pipeline de despliegue automático.
- Documentación de progreso actualizada.

---

## 8. Documentos del Sprint 1

Generados:
- `docs/arquitectura/arquitectura.md` — especificación de componentes.
- `docs/decisiones/decisiones.md` — justificación de tecnologías.
- `docs/api/api.md` — especificación API preliminar.
- `docs/analisis/problema-empresarial.md` — análisis del caso.
- `docs/diagramas/arquitectura.png` — diagrama de arquitectura.
- `.github/workflows/ci.yml` — pipeline de validación.

Pendientes para Sprint 2:
- `docs/seguridad/keyvault.md` — documentación de Key Vault.
- `docs/deployment/github-actions.md` — guía de CI/CD.
- `docs/tests/test-plan.md` — plan de pruebas.

---

## 9. Cronograma Actual vs Planificado

Hito: Sprint 1 completo. Planificado: 10 Mar. Real: 10 Mar. Estado: On time.
Hito: API funcional. Planificado: 24 Mar. Real: 24 Mar. Estado: En progreso.
Hito: Despliegue Azure. Planificado: 24 Mar. Real: 24 Mar. Estado: En progreso.
Hito: IA mínima. Planificado: 21 Abr. Real: 21 Abr. Estado: Planeado.
Hito: Entrega final. Planificado: 15 Jun. Real: 15 Jun. Estado: Planeado.

---

## 10. Observaciones finales

Evaluación general del Sprint: 9/10.

Puntos fuertes:
- Arquitectura definida y documentada.
- Alineación con los requisitos del tutor.
- Uso de herramientas profesionales: Git, SonarQube y Azure.
- Documentación técnica relevante.

Áreas de mejora:
- Avanzar con la implementación de código en Sprint 2.
- Incrementar el enfoque en testing.
- Acelerar la integración de la clasificación automática.

Confianza en el éxito del TFG: alta, con el enfoque y la estructura actuales.
