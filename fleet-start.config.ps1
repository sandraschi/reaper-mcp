# Per-repo fleet start config for reaper-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'reaper-mcp'
    BackendPort  = 10797
    FrontendPort = 10796
    HealthPath   = '/health'
    WebRoot      = 'D:\Dev\repos\reaper-mcp\web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'reaper_mcp.server:app'
        SyncExtras    = @('dev')
        Env           = @{ WEB_PORT = '10797' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
