# Ejecuta pruebas con cobertura y publica el analisis en SonarQube Cloud.
# El token se solicita de forma oculta y solo permanece en memoria.

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ScannerVersion = "8.1.0.6389"
$ScannerName = "sonar-scanner-$ScannerVersion-windows-x64"
$ToolsDirectory = Join-Path $RepoRoot ".tools"
$ScannerDirectory = Join-Path $ToolsDirectory $ScannerName
$ScannerExecutable = Join-Path $ScannerDirectory "bin\sonar-scanner.bat"
$ScannerArchive = Join-Path $ToolsDirectory "$ScannerName.zip"
$ScannerUrl = "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$ScannerVersion-windows-x64.zip"
$CoverageReport = Join-Path $RepoRoot "coverage.xml"

function Resolve-Python311 {
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "python"
    )

    foreach ($candidate in $candidates) {
        if ($candidate -eq "python") {
            $command = Get-Command python -ErrorAction SilentlyContinue
            if ($command) {
                return $command.Source
            }
        }
        elseif (Test-Path $candidate) {
            return $candidate
        }
    }

    throw "Python 3.11 no esta disponible."
}

function Install-SonarScanner {
    if (Test-Path $ScannerExecutable) {
        return
    }

    New-Item -ItemType Directory -Path $ToolsDirectory -Force | Out-Null
    Write-Host "Descargando SonarScanner CLI $ScannerVersion..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $ScannerUrl -OutFile $ScannerArchive
    try {
        Expand-Archive -LiteralPath $ScannerArchive -DestinationPath $ToolsDirectory -Force
    }
    finally {
        Remove-Item -LiteralPath $ScannerArchive -Force -ErrorAction SilentlyContinue
    }
}

$Python = Resolve-Python311
Install-SonarScanner

Push-Location $RepoRoot
try {
    Write-Host "Python: $Python" -ForegroundColor DarkGray
    Write-Host "Instalando dependencias de pruebas..." -ForegroundColor Cyan
    & $Python -m pip install -r requirements-dev.txt
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudieron instalar las dependencias."
    }

    Write-Host "Ejecutando 14 pruebas y generando coverage.xml..." -ForegroundColor Cyan
    & $Python -m coverage erase
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo limpiar la cobertura anterior."
    }
    & $Python -m coverage run -m unittest discover -s tests -p "test_*.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Las pruebas no han finalizado correctamente."
    }
    & $Python -m coverage report
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo generar el resumen de cobertura."
    }
    & $Python -m coverage xml -o $CoverageReport
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $CoverageReport)) {
        throw "No se pudo generar coverage.xml."
    }
    Write-Host "Informe generado: $CoverageReport" -ForegroundColor DarkGray

    $previousToken = $env:SONAR_TOKEN
    if (-not $env:SONAR_TOKEN) {
        $secureToken = Read-Host "Token de SonarQube Cloud" -AsSecureString
        $credential = [System.Management.Automation.PSCredential]::new("sonar", $secureToken)
        $env:SONAR_TOKEN = $credential.GetNetworkCredential().Password
    }

    try {
        Write-Host "Publicando analisis y cobertura en SonarQube Cloud..." -ForegroundColor Cyan
        $scannerWork = Join-Path $RepoRoot ".scannerwork"
        if (Test-Path $scannerWork) {
            Remove-Item -LiteralPath $scannerWork -Recurse -Force
        }

        $scannerProcess = Start-Process `
            -FilePath "cmd.exe" `
            -ArgumentList @("/d", "/c", "`"$ScannerExecutable`"") `
            -WorkingDirectory $RepoRoot `
            -NoNewWindow `
            -Wait `
            -PassThru
        if ($scannerProcess.ExitCode -ne 0) {
            throw "SonarScanner finalizo con codigo $($scannerProcess.ExitCode)."
        }
        if (-not (Test-Path (Join-Path $scannerWork "report-task.txt"))) {
            throw "SonarScanner termino sin generar el comprobante de subida."
        }
    }
    finally {
        $env:SONAR_TOKEN = $previousToken
    }

    Write-Host "Analisis completado. Revisa el panel de SonarQube Cloud." -ForegroundColor Green
}
finally {
    Pop-Location
}
