#!/bin/bash

# Device Support Service - Docker Deployment Script
# This script simplifies Docker deployment for the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_info "Docker and Docker Compose are installed ✓"
}

check_env() {
    if [ ! -f ".env" ]; then
        print_warn ".env file not found. Creating from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_info "Created .env file. Please edit it with your API keys."
        else
            print_error "Neither .env nor .env.example found."
            exit 1
        fi
    else
        print_info ".env file found ✓"
    fi
}

build_image() {
    print_info "Building Docker image..."
    docker-compose build --no-cache
    print_info "Docker image built successfully ✓"
}

start_services() {
    print_info "Starting services..."
    docker-compose up -d
    print_info "Services started ✓"
    
    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 5
    
    # Check if Streamlit is running
    if docker-compose exec -T app curl -s http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        print_info "Streamlit app is ready ✓"
    else
        print_warn "Streamlit app may still be initializing, check logs"
    fi
}

stop_services() {
    print_info "Stopping services..."
    docker-compose down
    print_info "Services stopped ✓"
}

view_logs() {
    print_info "Viewing logs (press Ctrl+C to exit)..."
    docker-compose logs -f app
}

status() {
    print_info "Service Status:"
    docker-compose ps
}

clean_up() {
    print_warn "Cleaning up containers and volumes..."
    read -p "Are you sure? This will remove all data. (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        print_info "Cleanup complete ✓"
    else
        print_info "Cleanup cancelled"
    fi
}

push_to_registry() {
    print_info "Pushing image to registry..."
    
    read -p "Enter registry URL (e.g., docker.io, myregistry.azurecr.io): " registry
    read -p "Enter image name (e.g., device-support): " image_name
    read -p "Enter image tag (default: latest): " tag
    tag=${tag:-latest}
    
    full_image="${registry}/${image_name}:${tag}"
    print_info "Pushing ${full_image}..."
    
    docker tag device-support:latest ${full_image}
    docker push ${full_image}
    print_info "Image pushed successfully ✓"
}

# Main menu
show_menu() {
    echo ""
    echo "Device Support Service - Docker Management"
    echo "========================================="
    echo "1) Check prerequisites"
    echo "2) Check/Create .env configuration"
    echo "3) Build Docker image"
    echo "4) Start services"
    echo "5) Stop services"
    echo "6) View logs"
    echo "7) Service status"
    echo "8) Clean up (remove containers and volumes)"
    echo "9) Push image to registry"
    echo "10) Full deployment (check, build, start)"
    echo "0) Exit"
    echo ""
    read -p "Select an option (0-10): " choice
}

# Full deployment
full_deploy() {
    check_prerequisites
    check_env
    build_image
    start_services
    
    print_info ""
    print_info "========================================="
    print_info "Deployment Complete! 🎉"
    print_info "========================================="
    print_info "Access the application at:"
    print_info "  Web UI: http://localhost:8501"
    print_info "  Qdrant: http://localhost:6333/dashboard"
    print_info ""
    print_info "View logs: docker-compose logs -f app"
    print_info "Stop services: docker-compose down"
}

# Main script
while true; do
    show_menu
    
    case $choice in
        1) check_prerequisites ;;
        2) check_env ;;
        3) build_image ;;
        4) start_services ;;
        5) stop_services ;;
        6) view_logs ;;
        7) status ;;
        8) clean_up ;;
        9) push_to_registry ;;
        10) full_deploy ;;
        0) print_info "Exiting..."; exit 0 ;;
        *) print_error "Invalid option. Please try again." ;;
    esac
done
