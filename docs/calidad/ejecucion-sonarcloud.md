# Ejecución de SonarCloud

## Ejecución realizada

Se ha ejecutado la integración de SonarCloud mediante push a la rama `main`.

- Commit: `d743fe2 Documentar entrega y ejecucion de SonarCloud`
- Workflow: `SonarCloud Quality Analysis`
- Run: https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro/actions/runs/27755744301
- Fecha de ejecución: 18/06/2026

## Resultado

El workflow fue lanzado correctamente por GitHub tras el push, pero GitHub Actions no inició el job por un bloqueo de cuenta:

```text
The job was not started because your account is locked due to a billing issue.
```

Esto significa que la configuración del workflow existe y se dispara, pero la plataforma de GitHub Actions no permite ejecutar trabajos hasta resolver el bloqueo de facturación de la cuenta.

## Próximos pasos

1. Entrar en GitHub y resolver el aviso de facturación o bloqueo de Actions.
2. Comprobar que existe el secreto `SONAR_TOKEN` en `Settings -> Secrets and variables -> Actions`.
3. Volver a ejecutar el workflow `SonarCloud Quality Analysis`.
4. Guardar captura del Quality Gate de SonarCloud.
5. Añadir la URL del panel de SonarCloud al PDF final de enlaces.
