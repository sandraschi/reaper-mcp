Param([switch]$Headless)

# --- SOTA Headless Standard ---
if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {
    Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden
    exit
}
$WindowStyle = if ($Headless) { 'Hidden' } else { 'Normal' }
# ------------------------------

$WebPort = 10796
$BackendPort = 10797
$ProjectRoot = Split-Path -Parent $PSScriptRoot

function Clear-Port {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -gt 4 } | Select-Object -First 1
    if (-not $conn) { return $false }
    $pid = $conn.OwningProcess
    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
    $name = if ($proc) { $proc.ProcessName } else { "PID $pid" }
    Write-Host "Port $Port held by $name (PID: $pid). Freeing..." -ForegroundColor Yellow
    try { Stop-Process -Id $pid -Force -ErrorAction Stop; Start-Sleep 1; return $true } catch {}
    try { taskkill /F /PID $pid 2>&1 | Out-Null; Start-Sleep 1; return $true } catch {}
    Write-Host "  Could not free port $Port. Run as Admin: taskkill /F /PID $pid" -ForegroundColor Red
    return $false
}

Write-Host "`n=== Reaper MCP ===" -ForegroundColor Cyan
Write-Host "Ports: backend :$BackendPort | frontend :$WebPort`n" -ForegroundColor Gray

Clear-Port $WebPort | Out-Null

# 1. Setup
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend deps..." -ForegroundColor Cyan
    npm install
}

# 2. Backend: check if already running
$HealthUrl = "http://127.0.0.1:$BackendPort/health"
$backendUp = $false
try {
    $r = Invoke-WebRequest -Uri $HealthUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    if ($r.StatusCode -eq 200) { $backendUp = $true }
} catch {}

if ($backendUp) {
    Write-Host "Backend: already running on :$BackendPort" -ForegroundColor Green
} else {
    Clear-Port $BackendPort | Out-Null
    Write-Host "Backend: starting on :$BackendPort ..." -ForegroundColor Cyan
    $backendCmd = "Set-Location '$ProjectRoot'; uv run --project '$ProjectRoot' uvicorn reaper_mcp.server:app --host 127.0.0.1 --port $BackendPort --log-level info"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle $WindowStyle
    Start-Sleep 3
}

# 3. Frontend: check if Vite is already up
$WebUrl = "http://127.0.0.1:$WebPort/"
$viteUp = $false
try {
    $r = Invoke-WebRequest -Uri $WebUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    if ($r.StatusCode -eq 200) { $viteUp = $true }
} catch {}

if ($viteUp) {
    Write-Host "Frontend: already running on :$WebPort" -ForegroundColor Green
    Write-Host "Open $WebUrl in your browser." -ForegroundColor Gray
    exit 0
}

# 4. Start Vite
Write-Host "Frontend: starting Vite on :$WebPort ..." -ForegroundColor Green
$poll = "for (`$i = 0; `$i -lt 60; `$i++) { try { `$null = Invoke-WebRequest -Uri '$WebUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; Start-Process '$WebUrl'; exit } catch { Start-Sleep 1 } }"
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $poll
Write-Host "Browser will open automatically when ready." -ForegroundColor Gray
npm run dev -- --port $WebPort --host
