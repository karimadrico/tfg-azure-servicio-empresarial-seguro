# Despliegue de la API TFG en Azure App Service (Windows PowerShell)
# Uso: .\scripts\deploy-azure.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ResourceGroup = "rg-tfg-cloudautomation-dev"
$WebAppName = "app-tfg-incidencias-dev"
$StorageAccount = "sttfgincidenciasdev"
$KeyVaultName = "kv-tfg-incidencias-dev"
$AppInsightsName = "appi-tfg-incidencias-dev"
$CosmosAccountName = if ($env:COSMOS_ACCOUNT_NAME) { $env:COSMOS_ACCOUNT_NAME } else { "cosmos-tfg-kdr-2026" }
$CosmosDatabase = if ($env:COSMOS_DATABASE) { $env:COSMOS_DATABASE } else { "tfg-solicitudes" }
$CosmosContainer = if ($env:COSMOS_CONTAINER) { $env:COSMOS_CONTAINER } else { "solicitudes" }
$StorageMode = if ($env:STORAGE_MODE) { $env:STORAGE_MODE } else { "cosmos" }
if (-not $env:API_KEY) {
    throw "Define la variable de entorno API_KEY antes de desplegar."
}
$ApiKey = $env:API_KEY

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

function Join-ProcessArguments {
    param([string[]]$ArgumentList)

    $quoted = foreach ($arg in $ArgumentList) {
        if ($null -eq $arg) {
            '""'
        }
        elseif ($arg -match '[\s"]') {
            '"' + $arg.Replace('"', '\"') + '"'
        }
        else {
            $arg
        }
    }

    return ($quoted -join ' ')
}

$AzCli = Resolve-AzCli
Write-Host "Ruta detectada: $AzCli"

if (-not $AzCli.EndsWith(".cmd") -and (Test-Path "$AzCli.cmd")) {
    $AzCli = "$AzCli.cmd"
}

Write-Host "Ruta final: $AzCli"

function Invoke-Az {
    param([string[]]$AzArgs)

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $AzCli
    $psi.Arguments = Join-ProcessArguments $AzArgs
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true

    $process = [System.Diagnostics.Process]::Start($psi)
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()

    if ($process.ExitCode -ne 0) {
        $details = (($stdout, $stderr) | Where-Object { $_ } | ForEach-Object { $_.Trim() }) -join "`n"
        throw "Error ejecutando: $AzCli $($AzArgs -join ' ')`n$details"
    }

    return $stdout.TrimEnd()
}

function Invoke-AzInteractive {
    param([string[]]$AzArgs)

    & $AzCli @AzArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "El comando interactivo devolvio codigo $LASTEXITCODE. Se verificara la sesion igualmente..."
    }
}

Write-Host "Azure CLI: $AzCli" -ForegroundColor DarkGray

Write-Host "=== Despliegue API TFG en Azure ===" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup"
Write-Host "App Service:    $WebAppName"
Write-Host "Storage mode:   $StorageMode"
Write-Host ""

Write-Host "[1/7] Comprobando sesion en Azure..."
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

Write-Host "[2/7] Obteniendo configuracion de Storage y Key Vault..."
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
$kvId = Invoke-Az @(
    "keyvault", "show",
    "--name", $KeyVaultName,
    "--resource-group", $ResourceGroup,
    "--query", "id",
    "-o", "tsv"
)
$kvRbacEnabled = Invoke-Az @(
    "keyvault", "show",
    "--name", $KeyVaultName,
    "--resource-group", $ResourceGroup,
    "--query", "properties.enableRbacAuthorization",
    "-o", "tsv"
)

Write-Host "[3/8] Preparando Application Insights y Cosmos DB..."
foreach ($providerNamespace in @("Microsoft.Insights", "Microsoft.OperationalInsights", "Microsoft.DocumentDB")) {
    $providerState = Invoke-Az @(
        "provider", "show",
        "--namespace", $providerNamespace,
        "--query", "registrationState",
        "-o", "tsv"
    )
    if ($providerState -ne "Registered") {
        Write-Host "Registrando proveedor $providerNamespace en la suscripcion..."
        Invoke-Az @("provider", "register", "--namespace", $providerNamespace, "--wait") | Out-Null
    }
}

$appInsights = ""
try {
    $appInsights = Invoke-Az @(
        "resource", "show",
        "--resource-group", $ResourceGroup,
        "--resource-type", "Microsoft.Insights/components",
        "--name", $AppInsightsName,
        "--query", "id",
        "-o", "tsv"
    )
}
catch {
    $appInsights = ""
}

if (-not $appInsights) {
    Invoke-Az @(
        "resource", "create",
        "--resource-group", $ResourceGroup,
        "--resource-type", "Microsoft.Insights/components",
        "--name", $AppInsightsName,
        "--location", "swedencentral",
        "--properties", '{"Application_Type":"web"}'
    ) | Out-Null
}

$appInsightsConnectionString = Invoke-Az @(
    "resource", "show",
    "--resource-group", $ResourceGroup,
    "--resource-type", "Microsoft.Insights/components",
    "--name", $AppInsightsName,
    "--query", "properties.ConnectionString",
    "-o", "tsv"
)

$cosmosEndpoint = ""
$cosmosKey = ""
if ($StorageMode -eq "cosmos") {
    $cosmosAccount = ""
    try {
        $cosmosAccount = Invoke-Az @(
            "cosmosdb", "show",
            "--name", $CosmosAccountName,
            "--resource-group", $ResourceGroup,
            "--query", "name",
            "-o", "tsv"
        )
    }
    catch {
        $cosmosAccount = ""
    }

    if (-not $cosmosAccount) {
        Write-Host "Creando Cosmos DB con Free Tier: $CosmosAccountName"
        Invoke-Az @(
            "cosmosdb", "create",
            "--name", $CosmosAccountName,
            "--resource-group", $ResourceGroup,
            "--locations", "regionName=swedencentral", "failoverPriority=0", "isZoneRedundant=False",
            "--default-consistency-level", "Session",
            "--enable-free-tier", "true"
        ) | Out-Null
    }

    $databaseExists = Invoke-Az @(
        "cosmosdb", "sql", "database", "exists",
        "--account-name", $CosmosAccountName,
        "--resource-group", $ResourceGroup,
        "--name", $CosmosDatabase,
        "-o", "tsv"
    )
    if ($databaseExists -ne "true") {
        Invoke-Az @(
            "cosmosdb", "sql", "database", "create",
            "--account-name", $CosmosAccountName,
            "--resource-group", $ResourceGroup,
            "--name", $CosmosDatabase
        ) | Out-Null
    }

    $containerExists = Invoke-Az @(
        "cosmosdb", "sql", "container", "exists",
        "--account-name", $CosmosAccountName,
        "--resource-group", $ResourceGroup,
        "--database-name", $CosmosDatabase,
        "--name", $CosmosContainer,
        "-o", "tsv"
    )
    if ($containerExists -ne "true") {
        Invoke-Az @(
            "cosmosdb", "sql", "container", "create",
            "--account-name", $CosmosAccountName,
            "--resource-group", $ResourceGroup,
            "--database-name", $CosmosDatabase,
            "--name", $CosmosContainer,
            "--partition-key-path", "/tipo_solicitud",
            "--throughput", "400"
        ) | Out-Null
    }

    $cosmosEndpoint = Invoke-Az @(
        "cosmosdb", "show",
        "--name", $CosmosAccountName,
        "--resource-group", $ResourceGroup,
        "--query", "documentEndpoint",
        "-o", "tsv"
    )
    $cosmosKey = Invoke-Az @(
        "cosmosdb", "keys", "list",
        "--name", $CosmosAccountName,
        "--resource-group", $ResourceGroup,
        "--type", "keys",
        "--query", "primaryMasterKey",
        "-o", "tsv"
    )
}

Write-Host "[4/8] Habilitando Managed Identity en App Service..."
$identity = Invoke-Az @(
    "webapp", "identity", "assign",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--query", "principalId",
    "-o", "tsv"
)

Write-Host "[5/8] Configurando acceso de App Service a Key Vault..."
if ($kvRbacEnabled -eq "true") {
    Write-Host "Key Vault usa RBAC. Asignando rol Key Vault Secrets User..."
    try {
        Invoke-Az @(
            "role", "assignment", "create",
            "--assignee", $identity,
            "--role", "Key Vault Secrets User",
            "--scope", $kvId
        ) | Out-Null
    }
    catch {
        if ($_.Exception.Message -notmatch "RoleAssignmentExists") {
            throw
        }
        Write-Host "El rol Key Vault Secrets User ya estaba asignado."
    }
}
else {
    Invoke-Az @(
        "keyvault", "set-policy",
        "--name", $KeyVaultName,
        "--object-id", $identity,
        "--secret-permissions", "get", "list"
    ) | Out-Null
}

Invoke-Az @(
    "keyvault", "secret", "set",
    "--vault-name", $KeyVaultName,
    "--name", "api-key",
    "--value", $ApiKey
) | Out-Null

$settings = @(
    "webapp", "config", "appsettings", "set",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--settings",
    "STORAGE_MODE=$StorageMode",
    "AZURE_STORAGE_CONNECTION_STRING=$storageConn",
    "AZURE_STORAGE_CONTAINER=incidencias",
    "AZURE_STORAGE_BLOB=incidencias.json",
    "COSMOS_ENDPOINT=$cosmosEndpoint",
    "COSMOS_KEY=$cosmosKey",
    "COSMOS_DATABASE=$CosmosDatabase",
    "COSMOS_CONTAINER=$CosmosContainer",
    "KEY_VAULT_URL=$kvUrl",
    "KEY_VAULT_SECRET_NAME=api-key",
    "APPLICATIONINSIGHTS_CONNECTION_STRING=$appInsightsConnectionString",
    "API_KEY=",
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true",
    "WEBSITES_PORT=8000"
)

Write-Host "[6/8] Configurando variables de entorno..."
Invoke-Az $settings | Out-Null

Invoke-Az @(
    "webapp", "config", "set",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--startup-file", "gunicorn --bind=0.0.0.0:8000 --workers=2 app:app"
) | Out-Null

Write-Host "[7/8] Publicando codigo de src/..."
$zipPath = Join-Path $env:TEMP "tfg-api-deploy.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$srcRoot = Join-Path $RepoRoot "src"
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    Get-ChildItem -Path $srcRoot -Recurse -File |
        Where-Object {
            $_.FullName -notmatch "\\__pycache__\\" -and
            $_.Extension -ne ".pyc" -and
            $_.Name -notin @("run-local.ps1", "run-local.sh", "test_local_api.py")
        } |
        ForEach-Object {
            $relativePath = $_.FullName.Substring($srcRoot.Length).TrimStart("\", "/").Replace("\", "/")
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $relativePath) | Out-Null
        }
}
finally {
    $zip.Dispose()
}

Invoke-Az @(
    "webapp", "deployment", "source", "config-zip",
    "--name", $WebAppName,
    "--resource-group", $ResourceGroup,
    "--src", $zipPath
) | Out-Null

Write-Host "[8/8] Despliegue publicado. La verificacion se ejecuta con scripts/verify-azure.ps1."

$defaultHostName = Invoke-Az @("webapp", "show", "--name", $WebAppName, "--resource-group", $ResourceGroup, "--query", "defaultHostName", "-o", "tsv")
$url = "https://$defaultHostName"
Write-Host ""
Write-Host "Despliegue finalizado." -ForegroundColor Green
Write-Host "URL:     $url"
Write-Host "API Key: almacenada en Key Vault"
if ($StorageMode -eq "cosmos") {
    Write-Host "Cosmos:  $CosmosAccountName / $CosmosDatabase / $CosmosContainer"
}
Write-Host ""
Write-Host "Comprobacion:"
Write-Host "  Invoke-RestMethod $url/health"
Write-Host "  Start-Process $url/portal"
Write-Host ""
Write-Host "  Invoke-RestMethod -Method POST $url/solicitudes ``"
Write-Host "    -ContentType 'application/json' ``"
Write-Host "    -Body '{\"tipo_solicitud\":\"acceso\",\"titulo\":\"Acceso VPN\",\"descripcion\":\"Necesito acceso VPN al entorno cloud\",\"reportado_por\":\"kdr1001@alu.ubu.es\"}'"





