# SonarCloud / SonarQube

Este proyecto deja preparado SonarCloud como servicio gestionado de SonarQube para analizar calidad, mantenibilidad y seguridad del código. La ejecución del análisis debe realizarse antes de la entrega final para obtener la URL y las capturas de evidencia.

## Puesta en marcha

1. Entrar en https://sonarcloud.io con la cuenta de GitHub.
2. Crear/importar el proyecto `karimadrico/tfg-azure-servicio-empresarial-seguro`.
3. Configurar:
   - Organization: `karimadrico`
   - Project key: `karimadrico_tfg-azure-servicio-empresarial-seguro`
4. Crear un token en SonarCloud.
5. En GitHub, ir a `Settings` -> `Secrets and variables` -> `Actions`.
6. Crear el secreto `SONAR_TOKEN` con el token generado.
7. Ejecutar el workflow `SonarCloud Quality Analysis` desde GitHub Actions o hacer push a `feature/tfg-alineacion-final`/`main`.

## Evidencias para la memoria

Para la entrega conviene guardar una captura del panel de SonarCloud con:

- Quality Gate.
- Bugs.
- Vulnerabilities.
- Code Smells.
- Duplications.
- Security Hotspots.

Esa captura puede añadirse a `docs/arquitectura/` y citarse en la memoria como evidencia de calidad de código.
