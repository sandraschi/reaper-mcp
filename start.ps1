param([switch]$Headless, [switch]$BackendOnly, [switch]$NoBrowser)
$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $PSCommandPath
$BackendPort = 10797
$FrontendPort = 10796

Write-Host "=== reaper-mcp Startup ===" -ForegroundColor Cyan

# Kill zombies
Write-Host "-> Clearing port zombies..." -ForegroundColor Yellow
foreach ($port in @($BackendPort, $FrontendPort)) {
    Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
        ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}
Start-Sleep 1

# Start backend
Write-Host "-> Starting backend on port $BackendPort..." -ForegroundColor Yellow
$BackendProc = Start-Process -NoNewWindow -PassThru -FilePath "uv" -ArgumentList @(
    "run", "python", "-m", "reaper_mcp.server"
) -WorkingDirectory $ScriptRoot

# Health poll
for ($i = 0; $i -lt 30; $i++) {
    try { $r = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue; if ($r.StatusCode -eq 200) { Write-Host "  Backend ready!" -ForegroundColor Green; break } } catch {}
    Start-Sleep 1
}

# Start frontend
if (-not $Headless -and -not $BackendOnly) {
    $webRoot = Join-Path $ScriptRoot "web_sota"
    if (Test-Path "$webRoot\package.json") {
        Write-Host "-> Starting frontend on port $FrontendPort..." -ForegroundColor Yellow
        $FrontendProc = Start-Process -NoNewWindow -PassThru -FilePath "C:\Users\sandr\.bun\bin\bun.exe" -ArgumentList @("run", "dev") -WorkingDirectory $webRoot
        Start-Sleep 2
        if (-not $NoBrowser) { Start-Process "http://127.0.0.1:$FrontendPort" }
    }
}

Write-Host "=== reaper-mcp running ===" -ForegroundColor Cyan
Write-Host "  Backend: http://127.0.0.1:$BackendPort" -ForegroundColor Green
Write-Host "  Frontend: http://127.0.0.1:$FrontendPort" -ForegroundColor Green

try {
    while ($true) {
        if ($BackendProc.HasExited) { Write-Host "Backend exited ($($BackendProc.ExitCode))" -ForegroundColor Red; break }
        Start-Sleep 2
    }
} finally {
    if (-not $BackendProc.HasExited) { $BackendProc.Kill() }
    if ($FrontendProc -and -not $FrontendProc.HasExited) { $FrontendProc.Kill() }
}
