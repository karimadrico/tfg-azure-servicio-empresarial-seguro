"""Clasificador ligero de solicitudes TI con recomendación automática."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    prioridad: str
    clasificacion: str
    confianza: float
    tipo_solicitud: str
    recomendacion: str


HIGH_KEYWORDS = (
    "caido",
    "caído",
    "critico",
    "crítico",
    "urgente",
    "seguridad",
    "hackeo",
    "intrusion",
    "intrusión",
    "no responde",
    "indisponible",
    "bloqueado",
)

MEDIUM_KEYWORDS = (
    "error",
    "fallo",
    "lento",
    "timeout",
    "login",
    "acceso",
    "email",
    "correo",
)

INFRA_KEYWORDS = (
    "servidor",
    "base de datos",
    "red",
    "dns",
    "vpn",
    "azure",
    "storage",
    "infraestructura",
    "entorno",
)

SECURITY_KEYWORDS = (
    "seguridad",
    "credencial",
    "password",
    "contraseña",
    "token",
    "acceso no autorizado",
    "permiso",
)

SUPPORT_KEYWORDS = (
    "usuario",
    "soporte",
    "ayuda",
    "configuracion",
    "configuración",
    "manual",
)

ACCESS_KEYWORDS = ("acceso", "permiso", "rol", "cuenta", "login", "vpn")
ENVIRONMENT_KEYWORDS = ("entorno", "despliegue", "staging", "produccion", "producción", "azure")
APPLICATION_KEYWORDS = ("aplicacion", "aplicación", "app", "servicio", "api")
CONFIG_KEYWORDS = ("configuracion", "configuración", "parametro", "parámetro", "ajuste")

VALID_TIPOS = {"acceso", "entorno", "aplicacion", "configuracion", "incidencia"}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _score_keywords(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _detect_tipo_solicitud(text: str, tipo_manual: str | None) -> str:
    if tipo_manual in VALID_TIPOS:
        return tipo_manual

    scores = {
        "acceso": _score_keywords(text, ACCESS_KEYWORDS),
        "entorno": _score_keywords(text, ENVIRONMENT_KEYWORDS),
        "aplicacion": _score_keywords(text, APPLICATION_KEYWORDS),
        "configuracion": _score_keywords(text, CONFIG_KEYWORDS),
        "incidencia": _score_keywords(text, HIGH_KEYWORDS + MEDIUM_KEYWORDS),
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "incidencia"


def _build_recommendation(
    tipo_solicitud: str,
    clasificacion: str,
    prioridad: str,
) -> str:
    actions = {
        ("acceso", "seguridad"): "Revisar identidad en Azure AD y aplicar principio de mínimo privilegio.",
        ("acceso", "soporte"): "Validar solicitud con el responsable del área y conceder acceso temporal.",
        ("entorno", "infraestructura"): "Provisionar entorno mediante pipeline CI/CD y registrar en inventario cloud.",
        ("aplicacion", "infraestructura"): "Desplegar aplicación en App Service y validar conectividad.",
        ("configuracion", "soporte"): "Aplicar cambio controlado y documentar en el registro de configuración.",
        ("incidencia", "infraestructura"): "Escalar al equipo de operaciones cloud y monitorizar disponibilidad.",
        ("incidencia", "seguridad"): "Activar protocolo de respuesta a incidentes y rotar credenciales afectadas.",
    }
    key = (tipo_solicitud, clasificacion)
    base = actions.get(
        key,
        "Registrar la solicitud, asignar responsable y dar seguimiento hasta su cierre.",
    )

    if prioridad == "alta":
        return f"Prioridad alta: atender en menos de 4 horas. {base}"
    if prioridad == "media":
        return f"Prioridad media: resolver en la siguiente ventana operativa. {base}"
    return f"Prioridad baja: programar en backlog de soporte. {base}"


def classify_solicitud(
    titulo: str,
    descripcion: str,
    prioridad_manual: str | None = None,
    tipo_solicitud_manual: str | None = None,
) -> ClassificationResult:
    text = _normalize(f"{titulo} {descripcion}")
    tipo_solicitud = _detect_tipo_solicitud(text, tipo_solicitud_manual)

    if prioridad_manual in {"baja", "media", "alta"}:
        prioridad = prioridad_manual
        prioridad_confianza = 1.0
    else:
        high_score = _score_keywords(text, HIGH_KEYWORDS)
        medium_score = _score_keywords(text, MEDIUM_KEYWORDS)

        if high_score >= 2 or ("no funciona" in text and high_score >= 1):
            prioridad = "alta"
            prioridad_confianza = min(0.95, 0.7 + high_score * 0.08)
        elif high_score == 1 or medium_score >= 2:
            prioridad = "media"
            prioridad_confianza = min(0.9, 0.65 + medium_score * 0.07)
        else:
            prioridad = "baja"
            prioridad_confianza = 0.75

    security_score = _score_keywords(text, SECURITY_KEYWORDS)
    infra_score = _score_keywords(text, INFRA_KEYWORDS)
    support_score = _score_keywords(text, SUPPORT_KEYWORDS)

    scores = {
        "seguridad": security_score,
        "infraestructura": infra_score,
        "soporte": support_score,
    }
    clasificacion = max(scores, key=scores.get)
    top_score = scores[clasificacion]

    if top_score == 0:
        clasificacion = "general"
        categoria_confianza = 0.6
    else:
        categoria_confianza = min(0.95, 0.55 + top_score * 0.12)

    confianza = round((prioridad_confianza + categoria_confianza) / 2, 2)
    recomendacion = _build_recommendation(tipo_solicitud, clasificacion, prioridad)

    return ClassificationResult(
        prioridad=prioridad,
        clasificacion=clasificacion,
        confianza=confianza,
        tipo_solicitud=tipo_solicitud,
        recomendacion=recomendacion,
    )


def classify_incidencia(
    titulo: str,
    descripcion: str,
    prioridad_manual: str | None = None,
) -> ClassificationResult:
    return classify_solicitud(titulo, descripcion, prioridad_manual)
