# Verificacion rapida de la API desplegada en Azure
# Uso: .\scripts\verify-azure.ps1

$ErrorActionPreference = "Stop"

$BaseUrl = if ($env:BASE_URL) {
    $env:BASE_URL.TrimEnd("/")
}
else {
    "https://app-tfg-incidencias-dev-fme6drcgg6bwenbg.swedencentral-01.azurewebsites.net"
}
if (-not $env:API_KEY) {
    throw "Define la variable de entorno API_KEY antes de ejecutar la verificacion."
}
$ApiKey = $env:API_KEY
$Headers = @{ Authorization = "Bearer $ApiKey" }

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method = "GET",
        [string]$Path,
        [object]$Body = $null
    )

    Write-Output "-> $Name"
    $params = @{
        Uri = "$BaseUrl$Path"
        Method = $Method
        Headers = $Headers
    }
    if ($Body) {
        $params.ContentType = "application/json"
        $params.Body = ($Body | ConvertTo-Json -Compress)
    }

    $response = Invoke-RestMethod @params
    $response | ConvertTo-Json -Depth 6
    Write-Output ""
}

Write-Host "=== Verificacion API en Azure ===" -ForegroundColor Green
Write-Host "URL: $BaseUrl"
Write-Host ""

Test-Endpoint -Name "Estado del servicio" -Path "/"
Test-Endpoint -Name "Health check" -Path "/health"
Test-Endpoint -Name "Crear solicitud TI" -Method "POST" -Path "/solicitudes" -Body @{
    tipo_solicitud = "acceso"
    titulo = "Prueba tribunal"
    descripcion = "Solicito acceso VPN al entorno cloud de desarrollo"
    reportado_por = "karima@ubu.es"
}
Test-Endpoint -Name "Listar solicitudes" -Path "/solicitudes"
Test-Endpoint -Name "Metricas" -Path "/metricas"

Write-Host "Verificacion completada." -ForegroundColor Green
