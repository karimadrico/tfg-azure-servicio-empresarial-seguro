from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from config import Config


class IncidenciaStorage:
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        self._incidencias: list[dict[str, Any]] | None = None

    def load(self) -> list[dict[str, Any]]:
        if self.config.STORAGE_MODE == "azure" and self.config.AZURE_STORAGE_CONNECTION_STRING:
            self._incidencias = self._load_from_azure()
            return self._incidencias

        if self._incidencias is not None:
            return self._incidencias

        self._incidencias = self._load_from_local()

        return self._incidencias

    def save(self, incidencias: list[dict[str, Any]]) -> None:
        self._incidencias = incidencias

        if self.config.STORAGE_MODE == "azure" and self.config.AZURE_STORAGE_CONNECTION_STRING:
            self._save_to_azure(incidencias)
        else:
            self._save_to_local(incidencias)

    def _load_from_local(self) -> list[dict[str, Any]]:
        path = Path(self.config.LOCAL_DATA_FILE)
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_to_local(self, incidencias: list[dict[str, Any]]) -> None:
        path = Path(self.config.LOCAL_DATA_FILE)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(incidencias, handle, ensure_ascii=False, indent=2)

    def _load_from_azure(self) -> list[dict[str, Any]]:
        from azure.storage.blob import BlobServiceClient

        client = BlobServiceClient.from_connection_string(
            self.config.AZURE_STORAGE_CONNECTION_STRING
        )
        container = client.get_container_client(self.config.AZURE_STORAGE_CONTAINER)
        blob = container.get_blob_client(self.config.AZURE_STORAGE_BLOB)

        if not blob.exists():
            return []

        payload = blob.download_blob().readall().decode("utf-8")
        return json.loads(payload) if payload else []

    def _save_to_azure(self, incidencias: list[dict[str, Any]]) -> None:
        from azure.storage.blob import BlobServiceClient

        client = BlobServiceClient.from_connection_string(
            self.config.AZURE_STORAGE_CONNECTION_STRING
        )
        container = client.get_container_client(self.config.AZURE_STORAGE_CONTAINER)
        if not container.exists():
            container.create_container()

        blob = container.get_blob_client(self.config.AZURE_STORAGE_BLOB)
        payload = json.dumps(incidencias, ensure_ascii=False, indent=2)
        blob.upload_blob(payload, overwrite=True)
