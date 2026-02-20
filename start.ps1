$ErrorActionPreference = "Stop"

# Configuration
$port = 10793
$frontendPort = 10796 # Assuming frontend runs here based on walkthrough
$backendCmd = "fastmcp run server.py --transport sse --port $port"

Write-Host "🎵 Starting Reaper MCP (SOTA Setup)..." -ForegroundColor Cyan

# 1. Kill any existing processes on ports
function Kill-Port($p) {
    $tcp = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($tcp) {
        Write-Host "Killing process on port $p..." -ForegroundColor Yellow
        Stop-Process -Id $tcp.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

Kill-Port $port
Kill-Port $frontendPort

# 2. Start Backend
Write-Host "Starting Backend on port $port..." -ForegroundColor Green
$backendProcess = Start-Process -FilePath "uv" -ArgumentList "run", "fastmcp", "run", "server.py", "--transport", "sse", "--port", "$port" -PassThru -NoNewWindow

# 3. Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Set-Location "web_sota"
# We use 'cmd /c' to run npm so it doesn't block properly or opens in new window if needed, 
# but here we want it to run in parallel. 
# Actually, 'npm run dev' usually runs interactively. 
# Let's run it in a new window for the user to see logs.
Start-Process -FilePath "cmd" -ArgumentList "/c npm run dev -- --port $frontendPort"

# Wait for backend a bit
Start-Sleep -Seconds 5

Write-Host "✅ SOTA Stack Running!" -ForegroundColor Green
Write-Host "Backend: http://localhost:$port"
Write-Host "Frontend: http://localhost:$frontendPort"
