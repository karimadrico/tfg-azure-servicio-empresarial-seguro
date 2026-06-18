# SonarCloud / SonarQube

Este proyecto utiliza SonarCloud como servicio gestionado de SonarQube para analizar calidad, mantenibilidad y seguridad del código. La integración está conectada a GitHub Actions, de forma que el análisis se ejecuta desde el workflow `SonarCloud Quality Analysis`.

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

## Ejecución

La ejecución normal se realiza con un push a `main`:

```powershell
git add .
git commit -m "Actualizar documentacion y ejecutar analisis SonarCloud"
git push origin main
```

GitHub Actions ejecuta los siguientes pasos:

1. Descarga el repositorio.
2. Instala Python 3.11.
3. Instala dependencias desde `src/requirements.txt`.
4. Lanza las pruebas con `python -m unittest discover -s tests -p "test_*.py"`.
5. Ejecuta el escaneo de SonarCloud.

Si el workflow falla en el último paso, la causa más probable es que falte el secreto `SONAR_TOKEN` o que el proyecto no esté importado todavía en SonarCloud con la clave correcta.

## Evidencias para la memoria

Para la entrega conviene guardar una captura del panel de SonarCloud con:

- Quality Gate.
- Bugs.
- Vulnerabilities.
- Code Smells.
- Duplications.
- Security Hotspots.

Esa captura puede añadirse a `docs/arquitectura/` y citarse en la memoria como evidencia de calidad de código.

## Enlace previsto

Una vez importado y analizado, el panel queda accesible en:

https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro
