param(
    [switch]$SkipPipeline,
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..\..")
Set-Location $projectRoot

$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = "python"
}

Write-Host "Project root: $projectRoot"
Write-Host "Using Python: $pythonExe"

if (-not $SkipPipeline) {
    Write-Host "Running pipeline..."
    & $pythonExe -m agents.pipeline
    if ($LASTEXITCODE -ne 0) {
        throw "Pipeline run failed with exit code $LASTEXITCODE"
    }
    Write-Host "Pipeline completed successfully."
}

Write-Host "Starting Streamlit on port $Port ..."
& $pythonExe -m streamlit run ui/app.py --server.port $Port
