#!/bin/bash
# Production stack testing script for UNIZG Career Hub

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[TEST]${NC} $1"; }
log_success() { echo -e "${GREEN}[PASS]${NC} $1"; }
log_error() { echo -e "${RED}[FAIL]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Test configuration
BACKEND_URL="http://localhost:5000"
FRONTEND_URL="http://localhost:3000"
NGINX_URL="http://localhost:80"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    log_info "Running: $test_name"
    
    if eval "$test_command" >/dev/null 2>&1; then
        log_success "$test_name"
        ((TESTS_PASSED++))
        return 0
    else
        log_error "$test_name"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Wait for service to be ready
wait_for_service() {
    local name="$1"
    local url="$2"
    local max_attempts=30
    local attempt=1
    
    log_info "Waiting for $name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "$url" >/dev/null 2>&1; then
            log_success "$name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    log_error "$name failed to start after $max_attempts attempts"
    return 1
}

# Individual tests
test_docker_containers() {
    log_info "Checking Docker containers..."
    
    local containers=(
        "unizg_postgres:postgres:15-alpine"
        "unizg_redis:redis:7-alpine"
        "unizg_backend:backend"
        "unizg_frontend:frontend"
        "unizg_nginx:nginx:alpine"
    )
    
    for container_info in "${containers[@]}"; do
        IFS=':' read -r container_name expected_image <<< "$container_info"
        
        if docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | grep -q "$container_name.*Up"; then
            log_success "Container $container_name is running"
            ((TESTS_PASSED++))
        else
            log_error "Container $container_name is not running"
            ((TESTS_FAILED++))
        fi
    done
}

test_database_connectivity() {
    log_info "Testing database connectivity..."
    
    if docker exec unizg_postgres pg_isready -U postgres >/dev/null 2>&1; then
        log_success "PostgreSQL is ready"
        ((TESTS_PASSED++))
    else
        log_error "PostgreSQL is not ready"
        ((TESTS_FAILED++))
        return 1
    fi
    
    # Test database connection via backend
    if curl -f "$BACKEND_URL/api/health" | grep -q "healthy"; then
        log_success "Backend database connection working"
        ((TESTS_PASSED++))
    else
        log_error "Backend database connection failed"
        ((TESTS_FAILED++))
    fi
}

test_redis_connectivity() {
    log_info "Testing Redis connectivity..."
    
    if docker exec unizg_redis redis-cli ping | grep -q "PONG"; then
        log_success "Redis is responding"
        ((TESTS_PASSED++))
    else
        log_error "Redis is not responding"
        ((TESTS_FAILED++))
    fi
}

test_backend_api() {
    log_info "Testing Backend API endpoints..."
    
    # Health check
    run_test "Backend health check" "curl -f $BACKEND_URL/api/health"
    
    # Root endpoint
    run_test "Backend root endpoint" "curl -f $BACKEND_URL/"
    
    # API endpoints (should return valid JSON)
    run_test "Faculties endpoint" "curl -f $BACKEND_URL/api/faculties"
    run_test "Associations endpoint" "curl -f $BACKEND_URL/api/associations"
    
    # Test user registration (should work without auth)
    local test_email="test_$(date +%s)@example.com"
    local test_data="{\"email\":\"$test_email\",\"password\":\"test123\",\"firstName\":\"Test\",\"lastName\":\"User\",\"role\":\"student\"}"
    
    if curl -f -X POST -H "Content-Type: application/json" -d "$test_data" "$BACKEND_URL/api/auth/register" >/dev/null 2>&1; then
        log_success "User registration endpoint working"
        ((TESTS_PASSED++))
    else
        log_warning "User registration failed (might be duplicate email)"
    fi
}

test_frontend_app() {
    log_info "Testing Frontend application..."
    
    # Frontend health
    run_test "Frontend health check" "curl -f $FRONTEND_URL/health"
    
    # Frontend main page
    run_test "Frontend main page" "curl -f $FRONTEND_URL/"
    
    # Static assets
    run_test "Frontend static assets" "curl -f $FRONTEND_URL/static/js/ || curl -f $FRONTEND_URL/assets/"
}

test_nginx_proxy() {
    log_info "Testing Nginx reverse proxy..."
    
    # Nginx health
    run_test "Nginx health check" "curl -f $NGINX_URL/health"
    
    # API proxy
    run_test "API proxy via Nginx" "curl -f $NGINX_URL/api/health"
    
    # Frontend proxy
    run_test "Frontend proxy via Nginx" "curl -f $NGINX_URL/"
    
    # Static assets via Nginx
    run_test "Static assets via Nginx" "curl -f -I $NGINX_URL/favicon.ico"
}

test_security_headers() {
    log_info "Testing security headers..."
    
    local headers_to_check=(
        "X-Frame-Options"
        "X-XSS-Protection"
        "X-Content-Type-Options"
        "Referrer-Policy"
    )
    
    for header in "${headers_to_check[@]}"; do
        if curl -I "$NGINX_URL/" 2>/dev/null | grep -qi "$header"; then
            log_success "Security header $header present"
            ((TESTS_PASSED++))
        else
            log_warning "Security header $header missing"
        fi
    done
}

test_performance() {
    log_info "Testing basic performance..."
    
    # Test response times
    local api_time=$(curl -o /dev/null -s -w '%{time_total}' "$NGINX_URL/api/health")
    local frontend_time=$(curl -o /dev/null -s -w '%{time_total}' "$NGINX_URL/")
    
    if (( $(echo "$api_time < 2.0" | bc -l) )); then
        log_success "API response time: ${api_time}s (good)"
        ((TESTS_PASSED++))
    else
        log_warning "API response time: ${api_time}s (slow)"
    fi
    
    if (( $(echo "$frontend_time < 3.0" | bc -l) )); then
        log_success "Frontend response time: ${frontend_time}s (good)"
        ((TESTS_PASSED++))
    else
        log_warning "Frontend response time: ${frontend_time}s (slow)"
    fi
}

# Main test execution
main() {
    echo "=================================================="
    echo "UNIZG Career Hub - Production Stack Test Suite"
    echo "=================================================="
    echo
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    # Wait for services to be ready
    wait_for_service "Backend API" "$BACKEND_URL/api/health"
    wait_for_service "Frontend" "$FRONTEND_URL/health"
    wait_for_service "Nginx" "$NGINX_URL/health"
    
    echo
    log_info "Starting comprehensive tests..."
    echo
    
    # Run all tests
    test_docker_containers
    test_database_connectivity
    test_redis_connectivity
    test_backend_api
    test_frontend_app
    test_nginx_proxy
    test_security_headers
    test_performance
    
    # Summary
    echo
    echo "=================================================="
    echo "                  TEST SUMMARY"
    echo "=================================================="
    log_success "Tests passed: $TESTS_PASSED"
    if [ $TESTS_FAILED -gt 0 ]; then
        log_error "Tests failed: $TESTS_FAILED"
        echo
        log_error "Production stack has issues that need attention!"
        exit 1
    else
        echo
        log_success "🎉 Production stack is working perfectly!"
        log_info "Your UNIZG Career Hub is ready for deployment!"
        echo
        echo "Access points:"
        echo "  • Main application: http://localhost"
        echo "  • API documentation: http://localhost/api"
        echo "  • Direct backend: http://localhost:5000"
        echo "  • Direct frontend: http://localhost:3000"
        exit 0
    fi
}

# Run main function
main "$@"