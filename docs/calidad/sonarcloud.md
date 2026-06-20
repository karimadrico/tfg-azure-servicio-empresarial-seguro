# SonarCloud / SonarQube Cloud

El proyecto utiliza SonarCloud como herramienta de revision de calidad interna del codigo. El analisis se realiza desde la interfaz web de SonarCloud conectada al repositorio de GitHub.

## Enlace del proyecto

https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

## Resultado observado

| Metrica | Resultado |
|---------|-----------|
| Puerta de calidad | Aprobada |
| Duplicacion | 0,0% |
| Lineas analizadas | 1,8k aprox. |
| Fiabilidad | A |
| Mantenibilidad | A, con 8 issues abiertos no bloqueantes |
| Seguridad | A |
| Issues de seguridad | 0 |
| Security Hotspots pendientes | 0 |
| Cobertura | No configurada |

## Evidencia para la entrega

Para UBUVirtual y defensa conviene guardar:

- captura del Quality Gate aprobado;
- captura del resumen de metricas generales;
- captura del análisis del 20 de junio (`docs/evidencias/sonarcloud-quality-gate-final-20junio.png`);
- enlace al panel de SonarCloud en el PDF final de enlaces.

## Interpretacion

SonarCloud aporta una medicion externa de mantenibilidad, fiabilidad, seguridad y duplicidad. El análisis del 20 de junio supera la puerta de calidad, no presenta problemas de seguridad ni fiabilidad y mantiene la duplicación en 0,0%. Los ocho issues abiertos pertenecen a mantenibilidad y no bloquean el Quality Gate. La cobertura permanece sin datos porque todavía no se importa el informe de las pruebas Python.

Los dos warnings del análisis no corresponden a defectos del código. SonarCloud solicitaba las versiones objetivo de Python y del proveedor Azure de Terraform. El fichero `sonar-project.properties` fija Python 3.11 y `azurerm` 3.100.0; el aviso debería desaparecer después del siguiente análisis del commit que incorpora esta configuración.

