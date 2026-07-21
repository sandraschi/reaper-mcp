# PowerShell test runner for Reaper MCP Server
# Runs unit and integration tests with proper Windows paths

param(
    [string]$TestType = "all",
    [switch]$Coverage,
    [switch]$Verbose,
    [string]$OutputDir = "test_results"
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Create output directory
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

# Function to run tests
function Run-Tests {
    param(
        [string]$TestPath,
        [string]$TestName,
        [string]$OutputFile
    )

    Write-Host "Running $TestName tests..." -ForegroundColor Cyan

    $pytestArgs = @(
        "-v"
        if ($Verbose) { "--tb=long" } else { "--tb=short" }
        if ($Coverage) {
            "--cov=reaper_mcp"
            "--cov-report=html:htmlcov"
            "--cov-report=xml:$OutputDir/coverage.xml"
            "--cov-report=term-missing"
        }
        $TestPath
    )

    # Remove empty strings from args
    $pytestArgs = $pytestArgs | Where-Object { $_ -ne "" }

    try {
        & python -m pytest $pytestArgs | Tee-Object -FilePath $OutputFile

        if ($LASTEXITCODE -eq 0) {
            Write-Host "âœ“ $TestName tests passed" -ForegroundColor Green
            return $true
        } else {
            Write-Host "âœ- $TestName tests failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "âœ- Error running $TestName tests: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main test execution
$allPassed = $true
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Run unit tests
if ($TestType -eq "all" -or $TestType -eq "unit") {
    $unitResult = Run-Tests -TestPath "tests/unit" -TestName "Unit" -OutputFile "$OutputDir/unit_tests_$timestamp.txt"
    $allPassed = $allPassed -and $unitResult
}

# Run integration tests
if ($TestType -eq "all" -or $TestType -eq "integration") {
    $integrationResult = Run-Tests -TestPath "tests/integration" -TestName "Integration" -OutputFile "$OutputDir/integration_tests_$timestamp.txt"
    $allPassed = $allPassed -and $integrationResult
}

# Generate coverage report if requested
if ($Coverage -and $allPassed) {
    Write-Host "`nGenerating coverage report..." -ForegroundColor Cyan

    if (Test-Path "htmlcov/index.html") {
        Write-Host "Coverage report available at: $(Resolve-Path htmlcov/index.html)" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n" + "=" * 50 -ForegroundColor Yellow
Write-Host "TEST SUMMARY" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow

if ($allPassed) {
    Write-Host "âœ“ All tests passed!" -ForegroundColor Green
    Write-Host "ðŸŽ¼ Ready for Austrian audio automation!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "âœ- Some tests failed. Check test output above." -ForegroundColor Red
    Write-Host "ðŸ“ Test results saved to: $OutputDir" -ForegroundColor Yellow
    exit 1
}
