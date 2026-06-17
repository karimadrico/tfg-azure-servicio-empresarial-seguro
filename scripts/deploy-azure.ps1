# Despliegue de la API TFG en Azure App Service (Windows PowerShell)
# Uso: .\scripts\deploy-azure.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ResourceGroup = "rg-tfg-cloudautomation-dev"
$WebAppName = "app-tfg-incidencias-dev"
$StorageAccount = "sttfgincidenciasdev"
$KeyVaultName = "kv-tfg-incidencias-dev"
$ApiKey = if ($env:API_KEY) { $env:API_KEY } else { "tfg-api-key-ubu-2026" }

function Resolve-AzCli {
    $command = Get-Command az.cmd -ErrorAction SilentlyContinue
    if (-not $command) {
        $command = Get-Command az -ErrorAction SilentlyContinue
    }

    if (-not $command) {
        throw "No se encontro Azure CLI. Instala Azure CLI o anade az.cmd al PATH."
    }

    $path = $command.Source
    if (-not $path.EndsWith(".cmd") -and (Test-Path "$path.cmd")) {
        $path = "$path.cmd"
    }

    return $path
}

$AzCli = Resolve-AzCli
Write-Host "Azure CLI: $AzCli"

function Invoke-Az {
    param([string[]]$AzArgs)

    $output = & $script:AzCli @AzArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Error ejecutando: $script:AzCli $($AzArgs -join ' ')`n$output"
    }

    return $output
}

Write-Host "=== Despliegue API TFG en Azure ===" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup"
Write-Host "App Service:    $WebAppName"
Write-Host ""

Write-Host "[1/6] Comprobando sesion en Azure..."
try {
    Invoke-Az @("account", "show", "--output", "none") | Out-Null
}
catch {
    Write-Host "No hay sesion activa. Ejecutando az login..."
    Invoke-Az @("login") | Out-Null
}

Write-Host "[2/6] Obteniendo configuracion de Storage y Key Vault..."
$storageConn = Invoke-Az @(
    "storage", "account", "show-connection-string",
    "--name", $StorageAccount,
    "--resource-group", $ResourceGroup,
    "--query", "connectionString",
    "-o", "tsv"
)
$kvUrl = Invoke-Az @(
    "keyvault", "show",
    "--name", $KeyVaultName,
    "--resource-group", $ResourceGroup,
    "--query", "properties.vaultUri",
    "-o", "tsv"
)

Write-Host "[3/6] Habilitando Managed Identity en App Service..."
$identity = Invoke-Az @(
    "webapp", "identity", "assign",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--query", "principalId",
    "-o", "tsv"
)

Write-Host "[4/6] Configurando acceso de App Service a Key Vault..."
Invoke-Az @(
    "keyvault", "set-policy",
    "--name", $KeyVaultName,
    "--object-id", $identity,
    "--secret-permissions", "get", "list"
) | Out-Null

Invoke-Az @(
    "keyvault", "secret", "set",
    "--vault-name", $KeyVaultName,
    "--name", "api-key",
    "--value", $ApiKey
) | Out-Null

Write-Host "[5/6] Configurando variables de entorno..."
Invoke-Az @(
    "webapp", "config", "appsettings", "set",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--settings",
    "STORAGE_MODE=azure",
    "AZURE_STORAGE_CONNECTION_STRING=$storageConn",
    "AZURE_STORAGE_CONTAINER=incidencias",
    "AZURE_STORAGE_BLOB=incidencias.json",
    "KEY_VAULT_URL=$kvUrl",
    "KEY_VAULT_SECRET_NAME=api-key",
    "API_KEY=",
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true",
    "WEBSITES_PORT=8000"
) | Out-Null

Invoke-Az @(
    "webapp", "config", "set",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--startup-file", "gunicorn --bind=0.0.0.0:8000 --workers=2 app:app"
) | Out-Null

Write-Host "[6/6] Publicando codigo de src/..."
$zipPath = Join-Path $env:TEMP "tfg-api-deploy.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path (Join-Path $RepoRoot "src\*") -DestinationPath $zipPath -Force

Invoke-Az @(
    "webapp", "deployment", "source", "config-zip",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--src", $zipPath
) | Out-Null

$url = "https://$WebAppName.azurewebsites.net"
Write-Host ""
Write-Host "Despliegue finalizado." -ForegroundColor Green
Write-Host "URL:     $url"
Write-Host "API Key: $ApiKey (almacenada en Key Vault)"
Write-Host ""
Write-Host "Comprobacion:"
Write-Host "  Invoke-RestMethod $url/health"
Write-Host ""
Write-Host "  Invoke-RestMethod -Method POST $url/incidencias ``"
Write-Host "    -Headers @{ Authorization = 'Bearer $ApiKey' } ``"
Write-Host "    -ContentType 'application/json' ``"
Write-Host "    -Body '{\"titulo\":\"Prueba Azure\",\"descripcion\":\"Servidor caido en produccion\",\"reportado_por\":\"karima@ubu.es\"}'"
