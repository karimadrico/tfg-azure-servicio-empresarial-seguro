# SonarCloud / SonarQube Cloud

El proyecto utiliza SonarCloud como herramienta de revision de calidad interna del codigo. El proyecto esta vinculado al repositorio de GitHub y el analisis se gestiona desde la interfaz web de SonarCloud, sin mantener un escaner local ni un workflow de pago.

## Enlace del proyecto

https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

## Resultado del ultimo analisis

| Metrica | Resultado |
|---------|-----------|
| Puerta de calidad | Pendiente de revisar cuatro alertas de Bicep |
| Duplicacion | 0,0% |
| Lineas analizadas | 3,5k aprox. |
| Fiabilidad | A |
| Bugs | 0 |
| Alertas abiertas | 4, limitadas a `Scope` y `Response` de Logic Apps |
| Security Hotspots pendientes | 0 |

Las cuatro alertas no afectan al codigo Python ni a Terraform. Son reglas genericas que
solicitan `secureData` en contenedores `Scope` y salidas `Response`; Azure Logic Apps
rechaza esas propiedades durante el despliegue. Las acciones HTTP internas si protegen
sus entradas y salidas, y ambos flujos se han validado mediante ejecuciones reales en Azure.
Antes de capturar el resultado definitivo deben revisarse en SonarCloud como excepciones
aceptadas, conservando esta justificacion tecnica.

## Evidencia para la entrega

Para UBUVirtual y defensa conviene guardar:

- captura del Quality Gate definitivo despues de revisar las cuatro excepciones;
- captura del resumen de metricas generales;
- captura del análisis del 20 de junio (`docs/evidencias/sonarcloud-quality-gate-final-20junio.png`);
- enlace al panel de SonarCloud en el PDF final de enlaces.

## Interpretacion

SonarCloud aporta una medicion externa de mantenibilidad, fiabilidad, seguridad y duplicacion. Esta revision se complementa con las 26 pruebas automaticas del repositorio, que se ejecutan localmente antes de publicar cambios relevantes.

## Revision desde la web

El panel se consulta directamente en SonarCloud después de sincronizar los cambios con GitHub. Las pruebas funcionales se ejecutan por separado mediante `unittest`, por lo que el repositorio no depende de GitHub Actions, runners facturables ni instalaciones locales de SonarScanner.

