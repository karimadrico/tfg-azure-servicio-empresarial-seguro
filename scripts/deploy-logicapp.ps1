# Despliega la Logic App sencilla del TFG.
# Uso:
#   $env:API_KEY = "<clave>"
#   .\scripts\deploy-logicapp.ps1

$ErrorActionPreference = "Stop"

$ResourceGroup = "rg-tfg-cloudautomation-dev"
$Location = "swedencentral"
$KeyVaultName = "kv-tfg-incidencias-dev"
$LogicAppName = "logic-tfg-solicitudes-dev"
$ApprovalLogicAppName = "logic-tfg-aprobaciones-dev"
$ApiBaseUrl = if ($env:BASE_URL) { $env:BASE_URL } else { "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net" }

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
        return $cmd.Source
    }

    throw "Azure CLI no encontrado."
}

$AzCli = Resolve-AzCli
$Template = Join-Path (Split-Path -Parent $PSScriptRoot) "infra\bicep\logicapp.bicep"
$ApprovalTemplate = Join-Path (Split-Path -Parent $PSScriptRoot) "infra\bicep\approval-logicapp.bicep"
$ApiKey = $env:API_KEY

if (-not $ApiKey) {
    Write-Output "API_KEY no esta definida. Leyendo secreto api-key desde Key Vault..."
    $ApiKey = & $AzCli keyvault secret show `
        --vault-name $KeyVaultName `
        --name api-key `
        --query value `
        -o tsv
    if ($LASTEXITCODE -ne 0 -or -not $ApiKey) {
        throw "No se pudo obtener API_KEY desde Key Vault. Define API_KEY manualmente."
    }
}

Write-Output "Desplegando Logic App $LogicAppName..."
& $AzCli deployment group create `
    --resource-group $ResourceGroup `
    --template-file $Template `
    --parameters location=$Location apiBaseUrl=$ApiBaseUrl apiKey=$ApiKey `
    --output table

if ($LASTEXITCODE -ne 0) {
    throw "No se pudo desplegar la Logic App."
}

Write-Output "Desplegando Logic App $ApprovalLogicAppName..."
& $AzCli deployment group create `
    --resource-group $ResourceGroup `
    --template-file $ApprovalTemplate `
    --parameters location=$Location apiBaseUrl=$ApiBaseUrl apiKey=$ApiKey `
    --output table

if ($LASTEXITCODE -ne 0) {
    throw "No se pudo desplegar la Logic App de aprobaciones."
}

$SubscriptionId = & $AzCli account show --query id -o tsv
$TriggerUrl = & $AzCli rest `
    --method post `
    --uri "https://management.azure.com/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.Logic/workflows/$LogicAppName/triggers/solicitud_http/listCallbackUrl?api-version=2019-05-01" `
    --query value `
    -o tsv
$ApprovalTriggerUrl = & $AzCli rest `
    --method post `
    --uri "https://management.azure.com/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.Logic/workflows/$ApprovalLogicAppName/triggers/decision_http/listCallbackUrl?api-version=2019-05-01" `
    --query value `
    -o tsv

Write-Output "Logic App desplegada."
if ($TriggerUrl) {
    Write-Output "URL del trigger HTTP:"
    Write-Output $TriggerUrl
}
else {
    Write-Output "No se pudo obtener la URL del trigger. Puedes copiarla desde Azure Portal."
}
if ($ApprovalTriggerUrl) {
    Write-Output "URL del trigger de decisiones (tratar como secreto):"
    Write-Output $ApprovalTriggerUrl
}
else {
    Write-Output "No se pudo obtener la URL del trigger de decisiones."
}
