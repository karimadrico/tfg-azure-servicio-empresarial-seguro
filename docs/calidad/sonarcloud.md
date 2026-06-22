# SonarCloud / SonarQube Cloud

El proyecto utiliza SonarCloud como herramienta de revision de calidad interna del codigo. El analisis se ejecuta mediante SonarScanner CLI para incorporar el informe de cobertura generado por las pruebas Python.

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
| Cobertura local | 88% sobre el codigo Python incluido |

## Evidencia para la entrega

Para UBUVirtual y defensa conviene guardar:

- captura del Quality Gate aprobado;
- captura del resumen de metricas generales;
- captura del análisis del 20 de junio (`docs/evidencias/sonarcloud-quality-gate-final-20junio.png`);
- enlace al panel de SonarCloud en el PDF final de enlaces.

## Interpretacion

SonarCloud aporta una medicion externa de mantenibilidad, fiabilidad, seguridad, duplicidad y cobertura. El analisis supera la puerta de calidad, no presenta issues abiertos ni hotspots pendientes y mantiene la duplicacion en 0,0%. Las catorce pruebas generan un informe XML con un 88% de cobertura local.

## Ejecucion manual

El analisis se publica sin GitHub Actions para evitar depender de facturacion o runners externos. Desde PowerShell se ejecuta:

```powershell
.\scripts\run-sonar-coverage.ps1
```

El script instala las dependencias de desarrollo, ejecuta las pruebas, genera `coverage.xml`, descarga SonarScanner CLI en `.tools/` y solicita el token de SonarQube Cloud de forma oculta. El token solo permanece en memoria durante el analisis.

