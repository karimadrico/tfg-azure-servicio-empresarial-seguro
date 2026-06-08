"""Clasificador ligero basado en reglas para prioridad y categoría."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ClassificationResult:
    prioridad: str
    clasificacion: str
    confianza: float


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
)

SECURITY_KEYWORDS = (
    "seguridad",
    "credencial",
    "password",
    "contraseña",
    "token",
    "acceso no autorizado",
)

SUPPORT_KEYWORDS = (
    "usuario",
    "soporte",
    "ayuda",
    "configuracion",
    "configuración",
    "manual",
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _score_keywords(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def classify_incidencia(
    titulo: str,
    descripcion: str,
    prioridad_manual: str | None = None,
) -> ClassificationResult:
    text = _normalize(f"{titulo} {descripcion}")

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
    return ClassificationResult(prioridad, clasificacion, confianza)
