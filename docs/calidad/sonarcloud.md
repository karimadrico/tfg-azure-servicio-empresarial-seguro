# Calidad del código con SonarCloud

El repositorio está vinculado al proyecto público de SonarCloud:

https://sonarcloud.io/project/overview?id=karimadrico_tfg-azure-servicio-empresarial-seguro

## Resultado del análisis del 30 de junio de 2026

| Métrica | Resultado |
|---------|-----------|
| Quality Gate | Aprobado |
| Problemas abiertos | 0 |
| Seguridad | A |
| Fiabilidad | A |
| Security Hotspots | 0 |
| Duplicación | 0,0 % |
| Líneas de código analizadas | 4,3 k |
| Cobertura importada | 0,0 % |

La cobertura aparece al 0,0 % porque este análisis web no recibió un informe de cobertura. La validación funcional se ejecuta de forma independiente mediante `unittest` y contiene 27 pruebas automáticas. Por tanto, la cifra de SonarCloud describe la ausencia de datos de cobertura importados, no la ausencia de pruebas en el repositorio.

![Quality Gate final aprobado](../evidencias/sonarcloud-quality-gate-final-30junio.png)

El análisis complementa las pruebas funcionales mediante reglas de seguridad, fiabilidad, mantenibilidad, duplicación y revisión de infraestructura como código. La captura conserva el estado observado después de incorporar la migración a Cosmos DB, la actualización documental y la verificación final del despliegue.

El proyecto utiliza la integración web de SonarCloud con GitHub. No mantiene un runner facturable ni guarda tokens de análisis en el repositorio.
