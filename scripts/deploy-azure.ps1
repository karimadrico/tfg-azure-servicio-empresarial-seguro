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
    $paths = @(
        "${env:ProgramFiles(x86)}\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
        "$env:ProgramFiles\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
    )

    foreach ($p in $paths) {
        if (Test-Path $p) {
            return $p
        }
    }

    $cmd = Get-Command az.cmd -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    $cmd = Get-Command az -ErrorAction SilentlyContinue
    if ($cmd) {
        $path = $cmd.Source
        if (-not $path.EndsWith(".cmd") -and (Test-Path "$path.cmd")) {
            $path = "$path.cmd"
        }
        return $path
    }

    throw "Azure CLI no encontrado. Instala Azure CLI o anade az.cmd al PATH."
}

$AzCli = Resolve-AzCli
Write-Host "Ruta detectada: $AzCli"

if (-not $AzCli.EndsWith(".cmd") -and (Test-Path "$AzCli.cmd")) {
    $AzCli = "$AzCli.cmd"
}

Write-Host "Ruta final: $AzCli"

function Invoke-Az {
    param([string[]]$AzArgs)

    $output = & $script:AzCli @AzArgs 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Error ejecutando: $script:AzCli $($AzArgs -join ' ')`n$output"
    }

    return $output
}

function Invoke-AzInteractive {
    param([string[]]$AzArgs)

    & $script:AzCli @AzArgs
    if ($LASTEXITCODE -ne 0) {
        throw "Error ejecutando: $script:AzCli $($AzArgs -join ' ')"
    }
}

Write-Host "Azure CLI: $AzCli" -ForegroundColor DarkGray

Write-Host "=== Despliegue API TFG en Azure ===" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup"
Write-Host "App Service:    $WebAppName"
Write-Host ""

Write-Host "[1/6] Comprobando sesion en Azure..."
try {
    Invoke-Az @("account", "show", "--query", "id", "-o", "tsv") | Out-Null
}
catch {
    Write-Host "No se pudo confirmar la sesion con az account show:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor DarkYellow
    Write-Host "Ejecutando az login --use-device-code..."
    Invoke-AzInteractive @("login", "--use-device-code")
    Invoke-Az @("account", "show", "--query", "id", "-o", "tsv") | Out-Null
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
Write-Host "  Start-Process $url/portal"
Write-Host ""
Write-Host "  Invoke-RestMethod -Method POST $url/solicitudes ``"
Write-Host "    -ContentType 'application/json' ``"
Write-Host "    -Body '{\"tipo_solicitud\":\"acceso\",\"titulo\":\"Acceso VPN\",\"descripcion\":\"Necesito acceso VPN al entorno cloud\",\"reportado_por\":\"kdr1001@alu.ubu.es\"}'"

