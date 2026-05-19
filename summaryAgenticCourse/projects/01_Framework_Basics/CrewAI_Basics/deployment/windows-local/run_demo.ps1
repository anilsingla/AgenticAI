param(
  [switch]
  $SkipRun,
  [string]
  $Entry = ""
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..\\..")
Set-Location $projectRoot

if (Test-Path ".venv\\Scripts\\python.exe") {
  $pythonExe = ".venv\\Scripts\\python.exe"
} else {
  $pythonExe = "python"
}

if ([string]::IsNullOrWhiteSpace($Entry)) {
  $candidates = @("ui/app.py","app.py","agent.py","basic_agent.py")
  foreach ($c in $candidates) { if (Test-Path $c) { $Entry = $c; break } }
}

if ($SkipRun) {
  Write-Host "SkipRun enabled. Working directory: $projectRoot"
  exit 0
}

if ([string]::IsNullOrWhiteSpace($Entry)) {
  Write-Error "No runnable entry file found. Set -Entry explicitly."
}

if ($Entry -eq "ui/app.py") {
  & $pythonExe -m streamlit run $Entry
} else {
  & $pythonExe $Entry
}

