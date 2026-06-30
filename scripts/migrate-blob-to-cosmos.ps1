# Migra las solicitudes existentes desde Azure Blob Storage a Azure Cosmos DB.
# Uso:
#   $env:COSMOS_ACCOUNT_NAME = "cosmos-tfg-kdr-2026"
#   .\scripts\migrate-blob-to-cosmos.ps1

$ErrorActionPreference = "Stop"

$ResourceGroup = if ($env:RESOURCE_GROUP) { $env:RESOURCE_GROUP } else { "rg-tfg-cloudautomation-dev" }
$StorageAccount = if ($env:AZURE_STORAGE_ACCOUNT) { $env:AZURE_STORAGE_ACCOUNT } else { "sttfgincidenciasdev" }
$StorageContainer = if ($env:AZURE_STORAGE_CONTAINER) { $env:AZURE_STORAGE_CONTAINER } else { "incidencias" }
$StorageBlob = if ($env:AZURE_STORAGE_BLOB) { $env:AZURE_STORAGE_BLOB } else { "incidencias.json" }
$CosmosAccountName = if ($env:COSMOS_ACCOUNT_NAME) { $env:COSMOS_ACCOUNT_NAME } else { "cosmos-tfg-kdr-2026" }
$CosmosDatabase = if ($env:COSMOS_DATABASE) { $env:COSMOS_DATABASE } else { "tfg-solicitudes" }
$CosmosContainer = if ($env:COSMOS_CONTAINER) { $env:COSMOS_CONTAINER } else { "solicitudes" }

function Resolve-AzCli {
    $paths = @(
        "${env:ProgramFiles(x86)}\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
        "$env:ProgramFiles\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
    )

    foreach ($path in $paths) {
        if (Test-Path $path) {
            return $path
        }
    }

    $cmd = Get-Command az.cmd -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    throw "Azure CLI no encontrado."
}

$AzCli = Resolve-AzCli

Write-Host "=== Migracion Blob Storage -> Cosmos DB ===" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Blob:           $StorageAccount/$StorageContainer/$StorageBlob"
Write-Host "Cosmos:         $CosmosAccountName/$CosmosDatabase/$CosmosContainer"
Write-Host ""

$storageConn = & $AzCli storage account show-connection-string `
    --name $StorageAccount `
    --resource-group $ResourceGroup `
    --query connectionString `
    -o tsv
if ($LASTEXITCODE -ne 0 -or -not $storageConn) {
    throw "No se pudo obtener la cadena de conexion de Storage."
}

$cosmosEndpoint = & $AzCli cosmosdb show `
    --name $CosmosAccountName `
    --resource-group $ResourceGroup `
    --query documentEndpoint `
    -o tsv
if ($LASTEXITCODE -ne 0 -or -not $cosmosEndpoint) {
    throw "No se pudo obtener el endpoint de Cosmos DB."
}

$cosmosKey = & $AzCli cosmosdb keys list `
    --name $CosmosAccountName `
    --resource-group $ResourceGroup `
    --type keys `
    --query primaryMasterKey `
    -o tsv
if ($LASTEXITCODE -ne 0 -or -not $cosmosKey) {
    throw "No se pudo obtener la clave de Cosmos DB."
}

$python = @(
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "python"
) | Where-Object { $_ -and (Get-Command $_ -ErrorAction SilentlyContinue) } | Select-Object -First 1
if (-not $python) {
    throw "No se encontro Python."
}

$env:AZURE_STORAGE_CONNECTION_STRING = $storageConn
$env:AZURE_STORAGE_CONTAINER = $StorageContainer
$env:AZURE_STORAGE_BLOB = $StorageBlob
$env:COSMOS_ENDPOINT = $cosmosEndpoint
$env:COSMOS_KEY = $cosmosKey
$env:COSMOS_DATABASE = $CosmosDatabase
$env:COSMOS_CONTAINER = $CosmosContainer

$script = @'
import json
import os

from azure.cosmos import CosmosClient, PartitionKey
from azure.storage.blob import BlobServiceClient

blob_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CONNECTION_STRING"]
).get_container_client(os.environ["AZURE_STORAGE_CONTAINER"]).get_blob_client(
    os.environ["AZURE_STORAGE_BLOB"]
)

if not blob_client.exists():
    records = []
else:
    payload = blob_client.download_blob().readall().decode("utf-8")
    records = json.loads(payload) if payload else []

client = CosmosClient(os.environ["COSMOS_ENDPOINT"], credential=os.environ["COSMOS_KEY"])
database = client.create_database_if_not_exists(id=os.environ["COSMOS_DATABASE"])
container = database.create_container_if_not_exists(
    id=os.environ["COSMOS_CONTAINER"],
    partition_key=PartitionKey(path="/tipo_solicitud"),
)

for record in records:
    if not record.get("id"):
        continue
    document = dict(record)
    document.setdefault("tipo_solicitud", "incidencia")
    container.upsert_item(document)

print(f"Solicitudes migradas: {len(records)}")
'@

$scriptPath = Join-Path $env:TEMP "migrate-blob-to-cosmos.py"
Set-Content -Path $scriptPath -Value $script -Encoding UTF8
& $python $scriptPath
if ($LASTEXITCODE -ne 0) {
    throw "La migracion no se completo correctamente."
}

Write-Host "Migracion completada." -ForegroundColor Green
