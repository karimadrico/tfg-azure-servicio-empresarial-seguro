import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

os.environ["STORAGE_MODE"] = "local"
os.environ["API_KEY"] = ""

import app as api_app
from classifier import classify_incidencia, classify_solicitud


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "incidencias.json"
        self.original_api_key = api_app.config.API_KEY
        api_app.config.API_KEY = ""
        api_app.config.LOCAL_DATA_FILE = str(self.data_file)
        api_app.storage.config.LOCAL_DATA_FILE = str(self.data_file)
        api_app.storage._incidencias = None
        self.client = api_app.app.test_client()

    def tearDown(self) -> None:
        api_app.config.API_KEY = self.original_api_key
        self.temp_dir.cleanup()

    def test_root_endpoint(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("mensaje", payload)
        self.assertEqual(payload["estado"], "operacional")

    def test_create_and_list_incidencia(self) -> None:
        create_response = self.client.post(
            "/incidencias",
            data=json.dumps(
                {
                    "titulo": "Servidor caído",
                    "descripcion": "El servidor principal no responde desde esta mañana",
                    "reportado_por": "usuario@empresa.com",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(create_response.status_code, 201)
        created = create_response.get_json()
        self.assertEqual(created["prioridad"], "alta")
        self.assertIn("recomendacion", created)
        self.assertIn("tipo_solicitud", created)

        list_response = self.client.get("/incidencias")
        self.assertEqual(list_response.status_code, 200)
        payload = list_response.get_json()
        self.assertEqual(payload["total"], 1)

    def test_create_solicitud_endpoint(self) -> None:
        response = self.client.post(
            "/solicitudes",
            data=json.dumps(
                {
                    "tipo_solicitud": "acceso",
                    "titulo": "Solicitud acceso VPN",
                    "descripcion": "Necesito acceso VPN al entorno de desarrollo cloud",
                    "reportado_por": "usuario@empresa.com",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["tipo_solicitud"], "acceso")
        self.assertTrue(payload["recomendacion"])

    def test_portal_endpoint(self) -> None:
        response = self.client.get("/portal")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Portal de Solicitudes TI", response.data)
        response.close()

    def test_service_catalog_endpoint(self) -> None:
        response = self.client.get("/catalogo")
        self.assertEqual(response.status_code, 200)
        services = response.get_json()["servicios"]
        self.assertGreaterEqual(len(services), 6)
        self.assertIn("vpn", {service["id"] for service in services})

    def test_request_links_service_asset_and_impact(self) -> None:
        response = self.client.post(
            "/solicitudes",
            json={
                "tipo_solicitud": "acceso",
                "titulo": "Acceso a la aplicacion financiera",
                "descripcion": "Necesito acceso operativo al portal financiero de produccion",
                "reportado_por": "finanzas@empresa.com",
                "servicio_id": "aplicacion-finanzas",
                "activo_id": "portal-finanzas",
                "entorno": "produccion",
            },
        )
        self.assertEqual(response.status_code, 201)
        created = response.get_json()
        self.assertEqual(created["servicio_id"], "aplicacion-finanzas")
        self.assertEqual(created["activo_id"], "portal-finanzas")
        self.assertEqual(created["impacto"], "critico")
        self.assertEqual(created["asignado_a"], "equipo_aplicaciones")

        invalid = self.client.post(
            "/solicitudes",
            json={
                "titulo": "Activo incorrecto",
                "descripcion": "El activo no pertenece al servicio seleccionado",
                "reportado_por": "usuario@empresa.com",
                "servicio_id": "vpn",
                "activo_id": "portal-finanzas",
                "entorno": "corporativo",
            },
        )
        self.assertEqual(invalid.status_code, 400)

    def test_sensitive_request_approval_workflow(self) -> None:
        created = self.client.post(
            "/solicitudes",
            json={
                "tipo_solicitud": "acceso",
                "titulo": "Acceso al portal financiero",
                "descripcion": "Solicito permisos para operar en el portal de produccion",
                "reportado_por": "analista@empresa.com",
                "servicio_id": "aplicacion-finanzas",
                "activo_id": "portal-finanzas",
                "entorno": "produccion",
            },
        ).get_json()
        self.assertEqual(created["estado"], "pendiente_aprobacion")
        self.assertEqual(created["estado_aprobacion"], "pendiente")

        notified = self.client.post(f"/solicitudes/{created['id']}/notificar-aprobacion")
        self.assertEqual(notified.status_code, 200)
        self.assertIsNotNone(notified.get_json()["notificacion_aprobacion"])

        approved = self.client.post(
            f"/solicitudes/{created['id']}/aprobacion",
            json={
                "decision": "aprobar",
                "actor": "responsable_finanzas",
                "comentario": "Acceso autorizado durante el cierre mensual.",
            },
        )
        self.assertEqual(approved.status_code, 200)
        self.assertEqual(approved.get_json()["estado"], "abierta")
        self.assertEqual(approved.get_json()["estado_aprobacion"], "aprobada")

    def test_escalation_updates_priority_owner_and_history(self) -> None:
        created = self.client.post(
            "/solicitudes",
            json={
                "titulo": "Servicio con degradacion continuada",
                "descripcion": "La degradacion afecta al trabajo diario del departamento",
                "reportado_por": "operaciones@empresa.com",
                "servicio_id": "correo",
                "activo_id": "buzon-usuario",
                "entorno": "corporativo",
            },
        ).get_json()
        escalated = self.client.post(
            f"/solicitudes/{created['id']}/escalar",
            json={"actor": "equipo_ti", "motivo": "Impacto creciente en varios usuarios"},
        )
        self.assertEqual(escalated.status_code, 200)
        payload = escalated.get_json()
        self.assertEqual(payload["prioridad"], "alta")
        self.assertEqual(payload["nivel_escalado"], 1)
        self.assertEqual(payload["asignado_a"], "equipo_colaboracion")
        self.assertEqual(payload["historial"][-1]["accion"], "escalado")

    def test_metricas(self) -> None:
        self.client.post(
            "/incidencias",
            data=json.dumps(
                {
                    "titulo": "Error login",
                    "descripcion": "No puedo acceder al sistema corporativo",
                    "reportado_por": "soporte@empresa.com",
                }
            ),
            content_type="application/json",
        )
        response = self.client.get("/metricas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["total_solicitudes"], 1)
        self.assertEqual(response.get_json()["sla"]["en_plazo"], 1)

    def test_ticket_lifecycle_and_history(self) -> None:
        created = self.client.post(
            "/solicitudes",
            json={
                "tipo_solicitud": "acceso",
                "titulo": "Acceso a producción",
                "descripcion": "Necesito acceso temporal al entorno de producción",
                "reportado_por": "tecnico@empresa.com",
            },
        ).get_json()

        response = self.client.patch(
            f"/solicitudes/{created['id']}",
            json={
                "estado": "en_proceso",
                "prioridad": "alta",
                "asignado_a": "equipo_seguridad",
                "comentario": "Identidad validada con el responsable.",
                "actor": "operador@empresa.com",
            },
        )

        self.assertEqual(response.status_code, 200)
        updated = response.get_json()
        self.assertEqual(updated["estado"], "en_proceso")
        self.assertEqual(updated["asignado_a"], "equipo_seguridad")
        self.assertEqual(updated["prioridad"], "alta")
        self.assertEqual(len(updated["historial"]), 2)
        self.assertIn("Identidad validada", updated["historial"][-1]["detalle"])

        detail = self.client.get(f"/solicitudes/{created['id']}")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.get_json()["id"], created["id"])

    def test_ticket_lifecycle_rejects_invalid_update(self) -> None:
        created = self.client.post(
            "/solicitudes",
            json={
                "titulo": "Revisión de permisos",
                "descripcion": "Revisar permisos del usuario en el portal interno",
                "reportado_por": "soporte@empresa.com",
            },
        ).get_json()

        response = self.client.patch(
            f"/solicitudes/{created['id']}",
            json={"estado": "eliminada"},
        )
        self.assertEqual(response.status_code, 400)

        missing = self.client.get("/solicitudes/SOL-999")
        self.assertEqual(missing.status_code, 404)


    def test_protected_endpoints_require_valid_token(self) -> None:
        api_app.config.API_KEY = "token-pruebas"

        self.assertEqual(self.client.get("/solicitudes").status_code, 401)
        self.assertEqual(
            self.client.get(
                "/solicitudes",
                headers={"Authorization": "Bearer incorrecto"},
            ).status_code,
            401,
        )
        authorized = self.client.get(
            "/solicitudes",
            headers={"Authorization": "Bearer token-pruebas"},
        )
        self.assertEqual(authorized.status_code, 200)

    def test_create_rejects_invalid_payloads(self) -> None:
        valid = {
            "titulo": "Solicitud válida",
            "descripcion": "Descripción suficientemente detallada",
            "reportado_por": "usuario@empresa.com",
        }
        invalid_payloads = (
            ({**valid, "titulo": ""}, "título"),
            ({**valid, "descripcion": "corta"}, "descripción"),
            ({**valid, "reportado_por": "correo-invalido"}, "email"),
            ({**valid, "prioridad": "urgente"}, "Prioridad"),
            ({**valid, "tipo_solicitud": "compra"}, "tipo_solicitud"),
        )

        for payload, expected_error in invalid_payloads:
            with self.subTest(expected_error=expected_error):
                response = self.client.post("/solicitudes", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertIn(expected_error, response.get_json()["error"])

    def test_list_filters_and_pagination_validation(self) -> None:
        for title, priority in (("Servidor crítico caído", "alta"), ("Consulta general", "baja")):
            self.client.post(
                "/solicitudes",
                json={
                    "titulo": title,
                    "descripcion": "Descripción operativa para probar los filtros",
                    "reportado_por": "filtros@empresa.com",
                    "prioridad": priority,
                },
            )

        filtered = self.client.get("/solicitudes?prioridad=alta&limit=1&offset=0")
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(filtered.get_json()["total"], 1)
        self.assertEqual(filtered.get_json()["resultados"][0]["prioridad"], "alta")

        invalid_queries = (
            "/solicitudes?estado=desconocido",
            "/solicitudes?prioridad=urgente",
            "/solicitudes?tipo_solicitud=compra",
            "/solicitudes?limit=101",
        )
        for url in invalid_queries:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 400)

    def test_update_validation_and_closed_transition(self) -> None:
        created = self.client.post(
            "/solicitudes",
            json={
                "titulo": "Revisión de acceso",
                "descripcion": "Validar el acceso temporal solicitado",
                "reportado_por": "operaciones@empresa.com",
            },
        ).get_json()
        url = f"/solicitudes/{created['id']}"

        invalid_updates = (
            ({"campo": "no permitido"}, 400),
            ({"asignado_a": ""}, 400),
            ({"comentario": "x" * 501}, 400),
            ({"estado": "abierta"}, 400),
        )
        for payload, status in invalid_updates:
            with self.subTest(payload=list(payload)):
                self.assertEqual(self.client.patch(url, json=payload).status_code, status)

        self.assertEqual(self.client.patch(url, json={"estado": "cerrada"}).status_code, 200)
        self.assertEqual(self.client.patch(url, json={"estado": "abierta"}).status_code, 409)

    def test_local_storage_can_reload_saved_data(self) -> None:
        expected = [{"id": "SOL-001", "estado": "abierta"}]
        api_app.storage.save(expected)
        api_app.storage._incidencias = None

        self.assertEqual(api_app.storage.load(), expected)

    def test_azure_storage_refreshes_data_on_each_load(self) -> None:
        config = SimpleNamespace(
            STORAGE_MODE="azure",
            AZURE_STORAGE_CONNECTION_STRING="UseDevelopmentStorage=true",
        )
        storage = api_app.IncidenciaStorage(config)
        first = [{"id": "SOL-001"}]
        updated = [*first, {"id": "SOL-002"}]

        with patch.object(storage, "_load_from_azure", side_effect=[first, updated]) as loader:
            self.assertEqual(storage.load(), first)
            self.assertEqual(storage.load(), updated)

        self.assertEqual(loader.call_count, 2)

    def test_operations_center_reports_workload_alerts_and_resolution(self) -> None:
        pending = self.client.post(
            "/solicitudes",
            json={
                "tipo_solicitud": "acceso",
                "titulo": "Acceso financiero pendiente",
                "descripcion": "Acceso requerido para el entorno financiero de produccion",
                "reportado_por": "control@empresa.com",
                "servicio_id": "aplicacion-finanzas",
                "activo_id": "api-finanzas",
                "entorno": "produccion",
            },
        ).get_json()
        regular = self.client.post(
            "/solicitudes",
            json={
                "titulo": "Consulta operativa",
                "descripcion": "Consulta general para probar el centro operativo",
                "reportado_por": "soporte@empresa.com",
            },
        ).get_json()
        self.client.patch(f"/solicitudes/{regular['id']}", json={"estado": "cerrada"})

        response = self.client.get("/operaciones")
        self.assertEqual(response.status_code, 200)
        summary = response.get_json()
        self.assertEqual(summary["total_solicitudes"], 2)
        self.assertEqual(summary["aprobaciones"]["pendientes"], 1)
        self.assertEqual(summary["por_impacto"]["critico"], 1)
        self.assertGreaterEqual(len(summary["alertas"]), 2)
        self.assertIn(pending["asignado_a"], summary["por_responsable"])
        self.assertGreaterEqual(summary["tiempo_medio_resolucion_horas"], 0)

    def test_demo_data_creates_complete_and_idempotent_scenario(self) -> None:
        first = self.client.post("/demo/cargar")
        self.assertEqual(first.status_code, 201)
        payload = first.get_json()
        self.assertEqual(payload["creadas"], 5)
        records = payload["solicitudes"]
        self.assertTrue(all(item["es_demo"] for item in records))
        self.assertIn("pendiente_aprobacion", {item["estado"] for item in records})
        self.assertIn("en_proceso", {item["estado"] for item in records})
        self.assertIn("cerrada", {item["estado"] for item in records})
        self.assertTrue(any(item["nivel_escalado"] == 1 for item in records))

        second = self.client.post("/demo/cargar")
        self.assertEqual(second.status_code, 200)
        self.assertEqual(second.get_json()["creadas"], 0)
        self.assertEqual(second.get_json()["existentes"], 5)

    def test_csv_report_is_protected_and_prevents_formula_injection(self) -> None:
        api_app.config.API_KEY = "token-pruebas"
        self.client.post(
            "/solicitudes",
            json={
                "titulo": "=SUM(1+1)",
                "descripcion": "Contenido usado para validar una exportacion segura",
                "reportado_por": "informe@empresa.com",
            },
        )
        self.assertEqual(self.client.get("/informes/solicitudes.csv").status_code, 401)
        response = self.client.get(
            "/informes/solicitudes.csv",
            headers={"Authorization": "Bearer token-pruebas"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response.content_type)
        self.assertIn(b"'=SUM(1+1)", response.data)


class ClassifierTests(unittest.TestCase):
    def test_security_classification(self) -> None:
        result = classify_incidencia(
            "Alerta de seguridad critica",
            "Se detecto un intento de intrusión y acceso no autorizado en el panel",
        )
        self.assertEqual(result.clasificacion, "seguridad")
        self.assertEqual(result.prioridad, "alta")
        self.assertTrue(result.recomendacion)

    def test_business_rule_scenarios(self) -> None:
        scenarios = (
            (
                "Alerta de seguridad crítica",
                "Intrusión y acceso no autorizado detectados",
                ("incidencia", "seguridad", "alta"),
            ),
            (
                "Error y fallo de conectividad",
                "El servidor VPN presenta error y fallo",
                ("incidencia", "infraestructura", "media"),
            ),
            (
                "Ayuda de configuración",
                "Necesito ayuda con la configuración manual de un usuario",
                ("configuracion", "soporte", "baja"),
            ),
            (
                "Consulta de calendario",
                "Quiero consultar el calendario de vacaciones",
                ("incidencia", "general", "baja"),
            ),
        )

        for titulo, descripcion, expected in scenarios:
            with self.subTest(titulo=titulo):
                result = classify_solicitud(titulo, descripcion)
                self.assertEqual(
                    (result.tipo_solicitud, result.clasificacion, result.prioridad),
                    expected,
                )


if __name__ == "__main__":
    unittest.main()
