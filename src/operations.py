"""Indicadores operativos, SLA y alertas de la plataforma TI."""

from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from typing import Any

UTC_OFFSET = "+00:00"


def build_csv_report(requests: list[dict[str, Any]]) -> str:
    fields = [
        "id", "titulo", "servicio", "activo", "entorno", "impacto",
        "prioridad", "estado", "estado_aprobacion", "asignado_a",
        "fecha_creacion", "fecha_objetivo_sla", "fecha_cierre", "nivel_escalado",
    ]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, delimiter=";", extrasaction="ignore")
    writer.writeheader()
    for item in requests:
        writer.writerow({field: _safe_csv_value(item.get(field, "")) for field in fields})
    return output.getvalue()


def _safe_csv_value(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return f"'{value}"
    return value


def build_operational_summary(
    requests: list[dict[str, Any]], now: datetime | None = None
) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    summary: dict[str, Any] = {
        "total_solicitudes": len(requests),
        "por_prioridad": {"baja": 0, "media": 0, "alta": 0},
        "por_estado": {
            "pendiente_aprobacion": 0,
            "abierta": 0,
            "en_proceso": 0,
            "cerrada": 0,
            "rechazada": 0,
        },
        "por_tipo_solicitud": {},
        "por_impacto": {"bajo": 0, "medio": 0, "alto": 0, "critico": 0},
        "por_responsable": {},
        "por_servicio": {},
        "sla": {"en_plazo": 0, "vencidas": 0, "cerradas": 0, "en_aprobacion": 0},
        "aprobaciones": {"pendientes": 0, "aprobadas": 0, "rechazadas": 0},
        "escaladas": 0,
        "tiempo_medio_resolucion_horas": 0.0,
        "satisfaccion": {
            "respuestas": 0,
            "promedio": 0.0,
            "total_puntos": 0,
            "distribucion": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
        },
        "alertas": [],
    }
    resolution_hours: list[float] = []
    for item in requests:
        _increment(summary["por_prioridad"], item.get("prioridad", "media"))
        _increment(summary["por_estado"], item.get("estado", "abierta"))
        _increment(summary["por_tipo_solicitud"], item.get("tipo_solicitud", "incidencia"))
        _increment(summary["por_impacto"], item.get("impacto", "bajo"))
        _increment(summary["por_responsable"], item.get("asignado_a", "sin_asignar"))
        _increment(summary["por_servicio"], item.get("servicio", "Servicio TI general"))
        _update_approval_metrics(summary, item)
        _update_sla_metrics(summary, item, current)
        _append_alerts(summary["alertas"], item, current)
        _update_satisfaction(summary["satisfaccion"], item)
        if int(item.get("nivel_escalado", 0)) > 0:
            summary["escaladas"] += 1
        resolution = _resolution_time(item)
        if resolution is not None:
            resolution_hours.append(resolution)

    if resolution_hours:
        summary["tiempo_medio_resolucion_horas"] = round(
            sum(resolution_hours) / len(resolution_hours), 2
        )
    satisfaction = summary["satisfaccion"]
    if satisfaction["respuestas"]:
        satisfaction["promedio"] = round(
            satisfaction["total_puntos"] / satisfaction["respuestas"], 2
        )
    satisfaction.pop("total_puntos")
    summary["alertas"].sort(key=lambda alert: (alert["orden"], alert["id"]))
    for alert in summary["alertas"]:
        alert.pop("orden", None)
    return summary


def _update_satisfaction(satisfaction: dict[str, Any], item: dict[str, Any]) -> None:
    rating = item.get("valoracion", {}).get("puntuacion")
    if not isinstance(rating, int) or isinstance(rating, bool) or rating not in range(1, 6):
        return
    satisfaction["respuestas"] += 1
    satisfaction["total_puntos"] += rating
    satisfaction["distribucion"][str(rating)] += 1


def _increment(values: dict[str, int], key: str) -> None:
    values[key] = values.get(key, 0) + 1


def _update_approval_metrics(summary: dict[str, Any], item: dict[str, Any]) -> None:
    approval = item.get("estado_aprobacion")
    mapping = {"pendiente": "pendientes", "aprobada": "aprobadas", "rechazada": "rechazadas"}
    if approval in mapping:
        summary["aprobaciones"][mapping[approval]] += 1


def _update_sla_metrics(
    summary: dict[str, Any], item: dict[str, Any], current: datetime
) -> None:
    state = item.get("estado", "abierta")
    if state in {"cerrada", "rechazada"}:
        summary["sla"]["cerradas"] += 1
        return
    if state == "pendiente_aprobacion":
        summary["sla"]["en_aprobacion"] += 1
        return
    deadline = _parse_timestamp(item.get("fecha_objetivo_sla"))
    bucket = "vencidas" if deadline and deadline < current else "en_plazo"
    summary["sla"][bucket] += 1


def _append_alerts(
    alerts: list[dict[str, Any]], item: dict[str, Any], current: datetime
) -> None:
    state = item.get("estado", "abierta")
    if state in {"cerrada", "rechazada"}:
        return
    base = {
        "id": item.get("id"),
        "titulo": item.get("titulo"),
        "responsable": item.get("asignado_a", "sin_asignar"),
        "servicio": item.get("servicio", "Servicio TI general"),
    }
    deadline = _parse_timestamp(item.get("fecha_objetivo_sla"))
    if state != "pendiente_aprobacion" and deadline and deadline < current:
        alerts.append({**base, "tipo": "sla_vencido", "nivel": "critico", "orden": 0})
    if item.get("estado_aprobacion") == "pendiente":
        alerts.append({**base, "tipo": "aprobacion_pendiente", "nivel": "alto", "orden": 1})
    if item.get("impacto") == "critico":
        alerts.append({**base, "tipo": "impacto_critico", "nivel": "alto", "orden": 2})
    if int(item.get("nivel_escalado", 0)) > 0:
        alerts.append({**base, "tipo": "solicitud_escalada", "nivel": "medio", "orden": 3})


def _resolution_time(item: dict[str, Any]) -> float | None:
    created = _parse_timestamp(item.get("fecha_creacion"))
    closed = _parse_timestamp(item.get("fecha_cierre"))
    if created is None or closed is None or closed < created:
        return None
    return (closed - created).total_seconds() / 3600


def _parse_timestamp(value: Any) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", UTC_OFFSET))
    except ValueError:
        return None
