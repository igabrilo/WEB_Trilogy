# Production stack testing script for UNIZG Career Hub (PowerShell)
param(
    [switch]$Quick,
    [switch]$Verbose
)

# Configuration
$BackendUrl = "http://localhost:5000"
$FrontendUrl = "http://localhost:3000"
$NginxUrl = "http://localhost:80"

# Counters
$TestsPassed = 0
$TestsFailed = 0

function Write-TestInfo { param($Message) Write-Host "[TEST] $Message" -ForegroundColor Blue }
function Write-TestPass { param($Message) Write-Host "[PASS] $Message" -ForegroundColor Green }
function Write-TestFail { param($Message) Write-Host "[FAIL] $Message" -ForegroundColor Red }
function Write-TestWarn { param($Message) Write-Host "[WARN] $Message" -ForegroundColor Yellow }

function Test-Service {
    param(
        [string]$Name,
        [string]$Url,
        [int]$TimeoutSec = 10
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec $TimeoutSec -ErrorAction Stop
        Write-TestPass "$Name is responding (Status: $($response.StatusCode))"
        $script:TestsPassed++
        return $true
    } catch {
        Write-TestFail "$Name is not responding: $($_.Exception.Message)"
        $script:TestsFailed++
        return $false
    }
}

function Wait-ForService {
    param(
        [string]$Name,
        [string]$Url,
        [int]$MaxAttempts = 30
    )
    
    Write-TestInfo "Waiting for $Name to be ready..."
    
    for ($i = 1; $i -le $MaxAttempts; $i++) {
        try {
            Invoke-WebRequest -Uri $Url -TimeoutSec 5 -ErrorAction Stop | Out-Null
            Write-TestPass "$Name is ready!"
            return $true
        } catch {
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        }
    }
    
    Write-TestFail "$Name failed to start after $MaxAttempts attempts"
    return $false
}

function Test-DockerContainers {
    Write-TestInfo "Checking Docker containers..."
    
    $containers = @(
        "unizg_postgres",
        "unizg_redis", 
        "unizg_backend",
        "unizg_frontend",
        "unizg_nginx"
    )
    
    foreach ($container in $containers) {
        try {
            $status = docker ps --filter "name=$container" --format "{{.Status}}"
            if ($status -match "Up") {
                Write-TestPass "Container $container is running"
                $script:TestsPassed++
            } else {
                Write-TestFail "Container $container is not running"
                $script:TestsFailed++
            }
        } catch {
            Write-TestFail "Error checking container $container: $($_.Exception.Message)"
            $script:TestsFailed++
        }
    }
}

function Test-DatabaseConnectivity {
    Write-TestInfo "Testing database connectivity..."
    
    try {
        $result = docker exec unizg_postgres pg_isready -U postgres 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-TestPass "PostgreSQL is ready"
            $script:TestsPassed++
        } else {
            Write-TestFail "PostgreSQL is not ready"
            $script:TestsFailed++
            return
        }
    } catch {
        Write-TestFail "Error checking PostgreSQL: $($_.Exception.Message)"
        $script:TestsFailed++
        return
    }
    
    # Test via backend health endpoint
    try {
        $response = Invoke-WebRequest -Uri "$BackendUrl/api/health" -TimeoutSec 10 -ErrorAction Stop
        $health = $response.Content | ConvertFrom-Json
        if ($health.status -eq "healthy") {
            Write-TestPass "Backend database connection working"
            $script:TestsPassed++
        } else {
            Write-TestFail "Backend reports database issues"
            $script:TestsFailed++
        }
    } catch {
        Write-TestFail "Backend health check failed: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

function Test-RedisConnectivity {
    Write-TestInfo "Testing Redis connectivity..."
    
    try {
        $result = docker exec unizg_redis redis-cli ping 2>$null
        if ($result -match "PONG") {
            Write-TestPass "Redis is responding"
            $script:TestsPassed++
        } else {
            Write-TestFail "Redis is not responding"
            $script:TestsFailed++
        }
    } catch {
        Write-TestFail "Error checking Redis: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

function Test-BackendAPI {
    Write-TestInfo "Testing Backend API endpoints..."
    
    # Health check
    Test-Service "Backend health check" "$BackendUrl/api/health"
    
    # Root endpoint  
    Test-Service "Backend root endpoint" "$BackendUrl/"
    
    # API endpoints
    Test-Service "Faculties endpoint" "$BackendUrl/api/faculties"
    Test-Service "Associations endpoint" "$BackendUrl/api/associations"
    
    # Test user registration
    try {
        $testEmail = "test_$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"
        $testData = @{
            email = $testEmail
            password = "test123"
            firstName = "Test"
            lastName = "User"
            role = "student"
        } | ConvertTo-Json
        
        $response = Invoke-WebRequest -Uri "$BackendUrl/api/auth/register" -Method POST -Body $testData -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
        Write-TestPass "User registration endpoint working"
        $script:TestsPassed++
    } catch {
        Write-TestWarn "User registration failed (might be expected): $($_.Exception.Message)"
    }
}

function Test-FrontendApp {
    Write-TestInfo "Testing Frontend application..."
    
    Test-Service "Frontend health check" "$FrontendUrl/health"
    Test-Service "Frontend main page" "$FrontendUrl/"
}

function Test-NginxProxy {
    Write-TestInfo "Testing Nginx reverse proxy..."
    
    Test-Service "Nginx health check" "$NginxUrl/health"
    Test-Service "API proxy via Nginx" "$NginxUrl/api/health"
    Test-Service "Frontend proxy via Nginx" "$NginxUrl/"
}

function Test-SecurityHeaders {
    Write-TestInfo "Testing security headers..."
    
    $headersToCheck = @(
        "X-Frame-Options",
        "X-XSS-Protection", 
        "X-Content-Type-Options",
        "Referrer-Policy"
    )
    
    try {
        $response = Invoke-WebRequest -Uri "$NginxUrl/" -Method HEAD -TimeoutSec 10 -ErrorAction Stop
        
        foreach ($header in $headersToCheck) {
            if ($response.Headers.ContainsKey($header)) {
                Write-TestPass "Security header $header present"
                $script:TestsPassed++
            } else {
                Write-TestWarn "Security header $header missing"
            }
        }
    } catch {
        Write-TestFail "Error checking security headers: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

function Test-Performance {
    Write-TestInfo "Testing basic performance..."
    
    try {
        # API response time
        $apiStart = Get-Date
        Invoke-WebRequest -Uri "$NginxUrl/api/health" -TimeoutSec 10 -ErrorAction Stop | Out-Null
        $apiTime = (Get-Date) - $apiStart
        
        if ($apiTime.TotalSeconds -lt 2.0) {
            Write-TestPass "API response time: $($apiTime.TotalSeconds.ToString('F2'))s (good)"
            $script:TestsPassed++
        } else {
            Write-TestWarn "API response time: $($apiTime.TotalSeconds.ToString('F2'))s (slow)"
        }
        
        # Frontend response time
        $frontendStart = Get-Date
        Invoke-WebRequest -Uri "$NginxUrl/" -TimeoutSec 10 -ErrorAction Stop | Out-Null
        $frontendTime = (Get-Date) - $frontendStart
        
        if ($frontendTime.TotalSeconds -lt 3.0) {
            Write-TestPass "Frontend response time: $($frontendTime.TotalSeconds.ToString('F2'))s (good)"
            $script:TestsPassed++
        } else {
            Write-TestWarn "Frontend response time: $($frontendTime.TotalSeconds.ToString('F2'))s (slow)"
        }
    } catch {
        Write-TestFail "Error testing performance: $($_.Exception.Message)"
        $script:TestsFailed++
    }
}

# Main execution
function Main {
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "UNIZG Career Hub - Production Stack Test Suite" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Check Docker
    try {
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-TestFail "Docker is not running. Please start Docker first."
            exit 1
        }
    } catch {
        Write-TestFail "Docker is not available. Please install and start Docker."
        exit 1
    }
    
    # Wait for services
    if (-not $Quick) {
        Wait-ForService "Backend API" "$BackendUrl/api/health" | Out-Null
        Wait-ForService "Frontend" "$FrontendUrl/health" | Out-Null  
        Wait-ForService "Nginx" "$NginxUrl/health" | Out-Null
    }
    
    Write-Host ""
    Write-TestInfo "Starting comprehensive tests..."
    Write-Host ""
    
    # Run tests
    Test-DockerContainers
    Test-DatabaseConnectivity
    Test-RedisConnectivity
    Test-BackendAPI
    Test-FrontendApp
    Test-NginxProxy
    Test-SecurityHeaders
    Test-Performance
    
    # Summary
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "                  TEST SUMMARY" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-TestPass "Tests passed: $TestsPassed"
    
    if ($TestsFailed -gt 0) {
        Write-TestFail "Tests failed: $TestsFailed"
        Write-Host ""
        Write-TestFail "Production stack has issues that need attention!"
        exit 1
    } else {
        Write-Host ""
        Write-Host "🎉 Production stack is working perfectly!" -ForegroundColor Green
        Write-TestInfo "Your UNIZG Career Hub is ready for deployment!"
        Write-Host ""
        Write-Host "Access points:" -ForegroundColor Yellow
        Write-Host "  • Main application: http://localhost" -ForegroundColor White
        Write-Host "  • API documentation: http://localhost/api" -ForegroundColor White
        Write-Host "  • Direct backend: http://localhost:5000" -ForegroundColor White
        Write-Host "  • Direct frontend: http://localhost:3000" -ForegroundColor White
        exit 0
    }
}

# Run main function
Main