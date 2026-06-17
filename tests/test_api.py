import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

os.environ["STORAGE_MODE"] = "local"
os.environ["API_KEY"] = ""

import app as api_app
from classifier import classify_incidencia


class ApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "incidencias.json"
        api_app.config.LOCAL_DATA_FILE = str(self.data_file)
        api_app.storage.config.LOCAL_DATA_FILE = str(self.data_file)
        api_app.storage._incidencias = None
        self.client = api_app.app.test_client()

    def tearDown(self) -> None:
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


class ClassifierTests(unittest.TestCase):
    def test_security_classification(self) -> None:
        result = classify_incidencia(
            "Intrusion critica detectada",
            "Se detecto un intento de intrusión urgente en el panel de administración",
        )
        self.assertEqual(result.clasificacion, "seguridad")
        self.assertEqual(result.prioridad, "alta")
        self.assertTrue(result.recomendacion)


if __name__ == "__main__":
    unittest.main()
