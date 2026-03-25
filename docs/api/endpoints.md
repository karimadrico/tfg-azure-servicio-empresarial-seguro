# API de Gestión de Incidencias

La aplicación expone una API REST desarrollada en Python utilizando Flask.

## Endpoints disponibles

### GET /

Devuelve información básica del servicio.

Respuesta:

{
  "mensaje": "API TFG Servicio Empresarial Seguro"
}

---

### GET /incidencias

Devuelve todas las incidencias registradas en el sistema.

Respuesta:

[
  {
    "titulo": "Error login",
    "descripcion": "No puedo acceder al sistema"
  }
]

---

### POST /incidencias

Permite registrar una nueva incidencia.

Ejemplo de petición:

POST /incidencias

{
  "titulo": "Servidor caído",
  "descripcion": "El servidor principal no responde"
}

Respuesta:

{
  "mensaje": "Incidencia creada"
}

---

### GET /metricas

Devuelve métricas básicas del sistema.

Respuesta:

{
  "total_incidencias": 3
}