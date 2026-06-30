import os


class Config:
    STORAGE_MODE = os.getenv("STORAGE_MODE", "local")
    LOCAL_DATA_FILE = os.getenv("LOCAL_DATA_FILE", "data/incidencias.json")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER", "incidencias")
    AZURE_STORAGE_BLOB = os.getenv("AZURE_STORAGE_BLOB", "incidencias.json")
    COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "")
    COSMOS_KEY = os.getenv("COSMOS_KEY", "")
    COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "tfg-solicitudes")
    COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "solicitudes")
    API_KEY = os.getenv("API_KEY", "")
    KEY_VAULT_URL = os.getenv("KEY_VAULT_URL", "")
    KEY_VAULT_SECRET_NAME = os.getenv("KEY_VAULT_SECRET_NAME", "api-key")
