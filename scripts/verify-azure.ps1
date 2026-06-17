# Verificacion rapida de la API desplegada en Azure
# Uso: .\scripts\verify-azure.ps1

$ErrorActionPreference = "Stop"

$BaseUrl = "https://app-tfg-incidencias-dev.azurewebsites.net"
$ApiKey = if ($env:API_KEY) { $env:API_KEY } else { "tfg-api-key-ubu-2026" }
$Headers = @{ Authorization = "Bearer $ApiKey" }

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Method = "GET",
        [string]$Path,
        [object]$Body = $null
    )

    Write-Host "-> $Name" -ForegroundColor Cyan
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
    Write-Host ""
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
