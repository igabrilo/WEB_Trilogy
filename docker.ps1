# UNIZG Career Hub - Docker Management Script for Windows PowerShell
# Usage: .\docker.ps1 [COMMAND]

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Arg1
)

# Configuration
$ProjectName = "unizg-career-hub"
$ComposeFileProd = "docker-compose.prod.yml"
$ComposeFileDev = "docker-compose.dev.yml"

# Helper functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if .env file exists
function Test-EnvFile {
    if (-not (Test-Path ".env")) {
        Write-Warning ".env file not found. Copying from template..."
        Copy-Item ".env.template" ".env"
        Write-Warning "Please edit .env file with your configuration before proceeding."
        return $false
    }
    return $true
}

# Development commands
function Start-Dev {
    Write-Info "Starting development environment..."
    if (-not (Test-EnvFile)) { return }
    
    docker-compose -f $ComposeFileDev up -d
    Write-Success "Development environment started!"
    Write-Info "Frontend: http://localhost:3000"
    Write-Info "Backend API: http://localhost:5000"
    Write-Info "Database: localhost:5432"
}

function Stop-Dev {
    Write-Info "Stopping development environment..."
    docker-compose -f $ComposeFileDev down
    Write-Success "Development environment stopped!"
}

function Restart-Dev {
    Write-Info "Restarting development environment..."
    Stop-Dev
    Start-Dev
}

function Show-DevLogs {
    docker-compose -f $ComposeFileDev logs -f
}

# Production commands
function Start-Prod {
    Write-Info "Starting production environment..."
    if (-not (Test-EnvFile)) { return }
    
    docker-compose -f $ComposeFileProd up -d
    Write-Success "Production environment started!"
    Write-Info "Application: http://localhost:80"
    Write-Info "API: http://localhost:80/api"
}

function Stop-Prod {
    Write-Info "Stopping production environment..."
    docker-compose -f $ComposeFileProd down
    Write-Success "Production environment stopped!"
}

function Restart-Prod {
    Write-Info "Restarting production environment..."
    Stop-Prod
    Start-Prod
}

function Show-ProdLogs {
    docker-compose -f $ComposeFileProd logs -f
}

# Build commands
function Build-All {
    Write-Info "Building all images..."
    docker-compose -f $ComposeFileProd build --no-cache
    Write-Success "All images built successfully!"
}

function Build-Backend {
    Write-Info "Building backend image..."
    docker-compose -f $ComposeFileProd build --no-cache backend
    Write-Success "Backend image built successfully!"
}

function Build-Frontend {
    Write-Info "Building frontend image..."
    docker-compose -f $ComposeFileProd build --no-cache frontend
    Write-Success "Frontend image built successfully!"
}

# Database commands
function Backup-Database {
    $BackupName = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"
    Write-Info "Creating database backup: $BackupName"
    
    if (-not (Test-Path "backup")) {
        New-Item -ItemType Directory -Path "backup"
    }
    
    docker-compose -f $ComposeFileProd exec postgres pg_dump -U postgres unizg_career_hub > "backup\$BackupName"
    Write-Success "Database backup created: backup\$BackupName"
}

function Restore-Database {
    param([string]$BackupFile)
    
    if (-not $BackupFile) {
        Write-Error "Please specify backup file: .\docker.ps1 db:restore backup_file.sql"
        return
    }
    
    if (-not (Test-Path "backup\$BackupFile")) {
        Write-Error "Backup file not found: backup\$BackupFile"
        return
    }
    
    $Response = Read-Host "This will overwrite the current database. Are you sure? (y/N)"
    if ($Response -match "^[yY]") {
        Write-Info "Restoring database from: $BackupFile"
        Get-Content "backup\$BackupFile" | docker-compose -f $ComposeFileProd exec -T postgres psql -U postgres unizg_career_hub
        Write-Success "Database restored successfully!"
    } else {
        Write-Info "Database restore cancelled."
    }
}

# Utility commands
function Clear-All {
    $Response = Read-Host "This will remove all containers, networks, and volumes. Are you sure? (y/N)"
    if ($Response -match "^[yY]") {
        Write-Info "Cleaning up Docker resources..."
        docker-compose -f $ComposeFileProd down -v --remove-orphans
        docker-compose -f $ComposeFileDev down -v --remove-orphans
        docker system prune -f
        Write-Success "Cleanup completed!"
    } else {
        Write-Info "Cleanup cancelled."
    }
}

function Show-Status {
    Write-Info "Production environment status:"
    docker-compose -f $ComposeFileProd ps
    Write-Host ""
    Write-Info "Development environment status:"
    docker-compose -f $ComposeFileDev ps
}

function Test-Health {
    Write-Info "Checking application health..."
    
    try {
        $BackendResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Success "Backend API: Healthy"
    } catch {
        Write-Error "Backend API: Unhealthy"
    }
    
    try {
        $FrontendResponse = Invoke-WebRequest -Uri "http://localhost:3000/health" -TimeoutSec 5 -ErrorAction Stop
        Write-Success "Frontend: Healthy"
    } catch {
        Write-Error "Frontend: Unhealthy"
    }
}

function Show-Help {
    Write-Host "UNIZG Career Hub - Docker Management Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\docker.ps1 [COMMAND]" -ForegroundColor White
    Write-Host ""
    Write-Host "Development Commands:" -ForegroundColor Yellow
    Write-Host "  dev:start     Start development environment"
    Write-Host "  dev:stop      Stop development environment"
    Write-Host "  dev:restart   Restart development environment"
    Write-Host "  dev:logs      Show development logs"
    Write-Host ""
    Write-Host "Production Commands:" -ForegroundColor Yellow
    Write-Host "  prod:start    Start production environment"
    Write-Host "  prod:stop     Stop production environment"
    Write-Host "  prod:restart  Restart production environment"
    Write-Host "  prod:logs     Show production logs"
    Write-Host ""
    Write-Host "Build Commands:" -ForegroundColor Yellow
    Write-Host "  build:all     Build all Docker images"
    Write-Host "  build:backend Build backend image only"
    Write-Host "  build:frontend Build frontend image only"
    Write-Host ""
    Write-Host "Database Commands:" -ForegroundColor Yellow
    Write-Host "  db:backup     Create database backup"
    Write-Host "  db:restore    Restore database from backup"
    Write-Host ""
    Write-Host "Utility Commands:" -ForegroundColor Yellow
    Write-Host "  status        Show containers status"
    Write-Host "  health        Check application health"
    Write-Host "  clean         Clean up all Docker resources"
    Write-Host "  help          Show this help message"
    Write-Host ""
}

# Main command router
switch ($Command.ToLower()) {
    "dev:start" { Start-Dev }
    "dev:stop" { Stop-Dev }
    "dev:restart" { Restart-Dev }
    "dev:logs" { Show-DevLogs }
    "prod:start" { Start-Prod }
    "prod:stop" { Stop-Prod }
    "prod:restart" { Restart-Prod }
    "prod:logs" { Show-ProdLogs }
    "build:all" { Build-All }
    "build:backend" { Build-Backend }
    "build:frontend" { Build-Frontend }
    "db:backup" { Backup-Database }
    "db:restore" { Restore-Database -BackupFile $Arg1 }
    "status" { Show-Status }
    "health" { Test-Health }
    "clean" { Clear-All }
    default { Show-Help }
}