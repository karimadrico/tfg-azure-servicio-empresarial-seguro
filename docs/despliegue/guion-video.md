# Guion del video de demostración

**TFG:** Cloud Computing: Análisis, Diseño y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure  
**Autora:** Karima Drafli Rico — Universidad de Burgos  
**Duración:** 6-8 minutos

---

## 1. Introducción (45 segundos)

> Hola, soy Karima Drafli Rico y presento mi Trabajo Fin de Grado del Grado en Ingeniería Informática de la Universidad de Burgos.
>
> El título del trabajo es *Cloud Computing: Análisis, Diseño y Despliegue de un Servicio Empresarial Seguro en Microsoft Azure*.
>
> En muchas empresas las incidencias técnicas se gestionan de forma manual, con correos o hojas de cálculo. He desarrollado una solución en Azure que permite registrar incidencias, clasificarlas de forma automática y almacenarlas de manera segura.

---

## 2. Arquitectura (1 minuto)

Mostrar en Azure Portal el resource group `rg-tfg-cloudautomation-dev` con estos recursos:

- `app-tfg-incidencias-dev` — API Flask en App Service
- `sttfgincidenciasdev` — Storage Account para persistencia
- `kv-tfg-incidencias-dev` — Key Vault para el token de autenticación
- `logic-tfg-provisionador-dev` — Logic App para automatizar el registro
- `ASP-rgtfgcloudautomationdev-b089` — plan de hospedaje

> La solución está desplegada en la suscripción Azure for Students. La API está desarrollada en Python con Flask. El clasificador analiza el texto de cada incidencia para asignar prioridad y categoría. El código fuente está en GitHub y el despliegue se automatiza con GitHub Actions.

Repositorio: https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro

---

## 3. Demostración de la API (2 minutos)

Terminal con la API en ejecucion:

```bash
curl http://localhost:5000/

curl -X POST http://localhost:5000/incidencias \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Servidor caido","descripcion":"El servidor principal no responde desde esta manana","reportado_por":"usuario@empresa.com"}'

curl http://localhost:5000/incidencias

curl http://localhost:5000/metricas
```

> En esta prueba el sistema detecta que se trata de un problema de infraestructura y asigna prioridad alta. La respuesta incluye la clasificación automática y el nivel de confianza.

Tambien muestro la misma operacion contra Azure:

```bash
curl https://app-tfg-incidencias-dev.azurewebsites.net/ \
  -H "Authorization: Bearer tfg-api-key-ubu-2026"
```

---

## 4. Logic App (1 minuto)

Abrir `logic-tfg-provisionador-dev` en Azure Portal y mostrar el flujo:

1. Trigger HTTP
2. Llamada a la API
3. Respuesta al cliente

> Con la Logic App un proceso externo puede registrar incidencias sin llamar directamente a la API. Esto automatiza parte del flujo operativo que planteé en el análisis del problema empresarial.

---

## 5. Repositorio y CI/CD (45 segundos)

En https://github.com/karimadrico/tfg-azure-servicio-empresarial-seguro muestro:

- `src/` — codigo de la API
- `tests/test_api.py` — pruebas unitarias
- `infra/terraform/` — infraestructura como código
- `.github/workflows/deploy.yml` — pipeline de despliegue

> Cada push a la rama main ejecuta las pruebas, valida Terraform y publica la API en App Service.

---

## 6. Cierre (30 segundos)

> Con este trabajo he analizado un proceso empresarial real, he diseñado una arquitectura cloud en Azure, he implementado un prototipo funcional con seguridad mediante Key Vault, despliegue automatizado y un componente de clasificación automática de incidencias.
>
> Muchas gracias por su atención.
