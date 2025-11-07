#!/bin/sh
# Docker entrypoint script for React frontend

# Enable strict error handling
set -e

# Function to log with timestamp
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting UNIZG Career Hub Frontend..."

# Replace environment variables in built files (for runtime configuration)
# This allows changing API_URL without rebuilding the image
if [ -n "$REACT_APP_API_URL" ]; then
    log "Configuring API URL: $REACT_APP_API_URL"
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|REACT_APP_API_URL_PLACEHOLDER|$REACT_APP_API_URL|g" {} \;
fi

if [ -n "$REACT_APP_ENVIRONMENT" ]; then
    log "Setting environment: $REACT_APP_ENVIRONMENT"
    find /usr/share/nginx/html -name "*.js" -exec sed -i "s|REACT_APP_ENVIRONMENT_PLACEHOLDER|$REACT_APP_ENVIRONMENT|g" {} \;
fi

# Create nginx cache directories
mkdir -p /var/cache/nginx/client_temp
mkdir -p /var/cache/nginx/proxy_temp
mkdir -p /var/cache/nginx/fastcgi_temp
mkdir -p /var/cache/nginx/uwsgi_temp
mkdir -p /var/cache/nginx/scgi_temp

# Set proper permissions
chown -R nginx:nginx /var/cache/nginx
chown -R nginx:nginx /usr/share/nginx/html

log "Frontend configured successfully!"
log "Starting Nginx..."

# Execute the main container command
exec "$@"