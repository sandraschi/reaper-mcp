set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
import 'scripts/just/fleet.just'

# --- Dashboard ---

# Open the interactive recipe dashboard in the browser
default:
    @just --list


# Synchronize deps, pre-commit hooks, and web frontend
bootstrap:
    uv sync --extra dev
    uv run pre-commit install
    Set-Location web_sota; npm ci; if ($LASTEXITCODE -ne 0) { npm install }
    Write-Host "Pre-commit hooks installed." -ForegroundColor Green
# --- Dev Commands ---

# Serve the MCP server
serve:
    Set-Location '{{justfile_directory()}}'
    uv run python -m reaper_mcp.server

# Run tests
test:
    Set-Location '{{justfile_directory()}}'
    uv run pytest tests/ -v

# Format Python code
fmt:
    Set-Location '{{justfile_directory()}}'
    uv run ruff format reaper_mcp/

# TypeScript typecheck
types:
    Set-Location '{{justfile_directory()}}\web_sota'
    npx tsc --noEmit

# All gates green: lint + types + test
gates-green: lint
    Set-Location '{{justfile_directory()}}'
    uv run pytest tests/ -q

# E2E Playwright tests
e2e:
    Set-Location '{{justfile_directory()}}\web_sota'
    npx playwright test

# --- Quality ---

# Execute Ruff SOTA v13.1 linting
lint:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check reaper_mcp/

# Execute Ruff SOTA v13.1 fix and formatting
fix:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check reaper_mcp/ --fix --unsafe-fixes
    uv run ruff format reaper_mcp/

# --- Tauri NSIS ---

# Build the Tauri NSIS desktop installer (full pipeline: frontend -> Rust -> NSIS)
build-native:
	$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
	$vcvars = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
	$envOutput = cmd /c "`"$vcvars`" > nul & set" | Where-Object { $_ -match '^(INCLUDE|LIB|LIBPATH|VCToolsVersion|WindowsSdkDir|UniversalCRTSdkDir|UCRTVersion)=' }
	foreach ($line in $envOutput) { $parts = $line.Split('=', 2); Set-Item -Path "env:$($parts[0])" -Value $parts[1] -ErrorAction SilentlyContinue }
	Set-Location '{{justfile_directory()}}\native'
	pwsh -NoProfile -File '{{justfile_directory()}}\native\build.ps1'

# Bootstrap: install dev deps + pre-commit hook
