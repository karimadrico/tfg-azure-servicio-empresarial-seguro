# SonarCloud / SonarQube Cloud

El proyecto utiliza SonarCloud como herramienta de revision de calidad interna del codigo. El proyecto esta vinculado al repositorio de GitHub y el analisis se gestiona desde la interfaz web de SonarCloud, sin mantener un escaner local ni un workflow de pago.

## Enlace del proyecto

https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

## Resultado observado

| Metrica | Resultado |
|---------|-----------|
| Puerta de calidad | Aprobada |
| Duplicacion | 0,0% |
| Lineas analizadas | 2,3k aprox. |
| Fiabilidad | A |
| Mantenibilidad | A, sin issues abiertos |
| Seguridad | A |
| Issues de seguridad | 0 |
| Security Hotspots pendientes | 0 |

## Evidencia para la entrega

Para UBUVirtual y defensa conviene guardar:

- captura del Quality Gate aprobado;
- captura del resumen de metricas generales;
- captura del análisis del 20 de junio (`docs/evidencias/sonarcloud-quality-gate-final-20junio.png`);
- enlace al panel de SonarCloud en el PDF final de enlaces.

## Interpretacion

SonarCloud aporta una medicion externa de mantenibilidad, fiabilidad, seguridad y duplicacion. Esta revision se complementa con las catorce pruebas automaticas del repositorio, que se ejecutan localmente antes de publicar cambios relevantes.

## Revision desde la web

El panel se consulta directamente en SonarCloud después de sincronizar los cambios con GitHub. Las pruebas funcionales se ejecutan por separado mediante `unittest`, por lo que el repositorio no depende de GitHub Actions, runners facturables ni instalaciones locales de SonarScanner.

