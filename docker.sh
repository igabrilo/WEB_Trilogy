#!/bin/bash
# Docker management script for UNIZG Career Hub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="unizg-career-hub"
COMPOSE_FILE_PROD="docker-compose.prod.yml"
COMPOSE_FILE_DEV="docker-compose.dev.yml"

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        log_warning ".env file not found. Copying from template..."
        cp .env.template .env
        log_warning "Please edit .env file with your configuration before proceeding."
        return 1
    fi
}

# Development commands
dev_start() {
    log_info "Starting development environment..."
    check_env_file
    docker-compose -f $COMPOSE_FILE_DEV up -d
    log_success "Development environment started!"
    log_info "Frontend: http://localhost:3000"
    log_info "Backend API: http://localhost:5000"
    log_info "Database: localhost:5432"
}

dev_stop() {
    log_info "Stopping development environment..."
    docker-compose -f $COMPOSE_FILE_DEV down
    log_success "Development environment stopped!"
}

dev_restart() {
    log_info "Restarting development environment..."
    dev_stop
    dev_start
}

dev_logs() {
    docker-compose -f $COMPOSE_FILE_DEV logs -f
}

# Production commands
prod_start() {
    log_info "Starting production environment..."
    check_env_file || return 1
    docker-compose -f $COMPOSE_FILE_PROD up -d
    log_success "Production environment started!"
    log_info "Application: http://localhost:80"
    log_info "API: http://localhost:80/api"
}

prod_stop() {
    log_info "Stopping production environment..."
    docker-compose -f $COMPOSE_FILE_PROD down
    log_success "Production environment stopped!"
}

prod_restart() {
    log_info "Restarting production environment..."
    prod_stop
    prod_start
}

prod_logs() {
    docker-compose -f $COMPOSE_FILE_PROD logs -f
}

# Build commands
build_all() {
    log_info "Building all images..."
    docker-compose -f $COMPOSE_FILE_PROD build --no-cache
    log_success "All images built successfully!"
}

build_backend() {
    log_info "Building backend image..."
    docker-compose -f $COMPOSE_FILE_PROD build --no-cache backend
    log_success "Backend image built successfully!"
}

build_frontend() {
    log_info "Building frontend image..."
    docker-compose -f $COMPOSE_FILE_PROD build --no-cache frontend
    log_success "Frontend image built successfully!"
}

# Database commands
db_backup() {
    local backup_name="backup_$(date +%Y%m%d_%H%M%S).sql"
    log_info "Creating database backup: $backup_name"
    
    mkdir -p ./backup
    docker-compose -f $COMPOSE_FILE_PROD exec postgres pg_dump -U postgres unizg_career_hub > "./backup/$backup_name"
    
    log_success "Database backup created: ./backup/$backup_name"
}

db_restore() {
    if [ -z "$1" ]; then
        log_error "Please specify backup file: ./docker.sh db:restore backup_file.sql"
        return 1
    fi
    
    if [ ! -f "./backup/$1" ]; then
        log_error "Backup file not found: ./backup/$1"
        return 1
    fi
    
    log_warning "This will overwrite the current database. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Restoring database from: $1"
        docker-compose -f $COMPOSE_FILE_PROD exec -T postgres psql -U postgres unizg_career_hub < "./backup/$1"
        log_success "Database restored successfully!"
    else
        log_info "Database restore cancelled."
    fi
}

# Utility commands
clean() {
    log_warning "This will remove all containers, networks, and volumes. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Cleaning up Docker resources..."
        docker-compose -f $COMPOSE_FILE_PROD down -v --remove-orphans
        docker-compose -f $COMPOSE_FILE_DEV down -v --remove-orphans
        docker system prune -f
        log_success "Cleanup completed!"
    else
        log_info "Cleanup cancelled."
    fi
}

status() {
    log_info "Production environment status:"
    docker-compose -f $COMPOSE_FILE_PROD ps
    echo
    log_info "Development environment status:"
    docker-compose -f $COMPOSE_FILE_DEV ps
}

health() {
    log_info "Checking application health..."
    
    if curl -f http://localhost:5000/api/health >/dev/null 2>&1; then
        log_success "Backend API: Healthy"
    else
        log_error "Backend API: Unhealthy"
    fi
    
    if curl -f http://localhost:3000/health >/dev/null 2>&1; then
        log_success "Frontend: Healthy"
    else
        log_error "Frontend: Unhealthy"
    fi
}

# Help function
show_help() {
    echo "UNIZG Career Hub - Docker Management Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Development Commands:"
    echo "  dev:start     Start development environment"
    echo "  dev:stop      Stop development environment"
    echo "  dev:restart   Restart development environment"
    echo "  dev:logs      Show development logs"
    echo
    echo "Production Commands:"
    echo "  prod:start    Start production environment"
    echo "  prod:stop     Stop production environment"
    echo "  prod:restart  Restart production environment"
    echo "  prod:logs     Show production logs"
    echo
    echo "Build Commands:"
    echo "  build:all     Build all Docker images"
    echo "  build:backend Build backend image only"
    echo "  build:frontend Build frontend image only"
    echo
    echo "Database Commands:"
    echo "  db:backup     Create database backup"
    echo "  db:restore    Restore database from backup"
    echo
    echo "Utility Commands:"
    echo "  status        Show containers status"
    echo "  health        Check application health"
    echo "  clean         Clean up all Docker resources"
    echo "  help          Show this help message"
    echo
}

# Main command router
case "$1" in
    "dev:start")
        dev_start
        ;;
    "dev:stop")
        dev_stop
        ;;
    "dev:restart")
        dev_restart
        ;;
    "dev:logs")
        dev_logs
        ;;
    "prod:start")
        prod_start
        ;;
    "prod:stop")
        prod_stop
        ;;
    "prod:restart")
        prod_restart
        ;;
    "prod:logs")
        prod_logs
        ;;
    "build:all")
        build_all
        ;;
    "build:backend")
        build_backend
        ;;
    "build:frontend")
        build_frontend
        ;;
    "db:backup")
        db_backup
        ;;
    "db:restore")
        db_restore "$2"
        ;;
    "status")
        status
        ;;
    "health")
        health
        ;;
    "clean")
        clean
        ;;
    "help"|""|*)
        show_help
        ;;
esac