#!/bin/bash
# Docker Validation Script
# Checks if Docker setup is correct before deployment

set -e

echo "=========================================="
echo "  Docker Setup Validation Script"
echo "=========================================="
echo ""

# Check 1: Docker installed
echo "[1/6] Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not installed"
    exit 1
fi
echo "✅ Docker: $(docker --version)"

# Check 2: Docker Compose installed
echo "[2/6] Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not installed"
    exit 1
fi
echo "✅ Docker Compose: $(docker-compose --version)"

# Check 3: .env file exists
echo "[3/6] Checking environment file..."
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "   Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created from .env.example"
        echo "   ⚠️  UPDATE .env WITH YOUR API KEYS!"
    else
        echo "❌ .env.example not found"
        exit 1
    fi
else
    echo "✅ .env file exists"
    # Check for required variables
    required_vars=("OPENAI_API_KEY" "QDRANT_API_KEY" "QDRANT_URL")
    for var in "${required_vars[@]}"; do
        if grep -q "^${var}=" .env; then
            value=$(grep "^${var}=" .env | cut -d'=' -f2)
            if [ -z "$value" ] || [ "$value" = "your-*-here" ]; then
                echo "⚠️  $var is not configured in .env"
            fi
        else
            echo "⚠️  $var missing from .env"
        fi
    done
fi

# Check 4: Dockerfile exists
echo "[4/6] Checking Dockerfile..."
if [ ! -f Dockerfile ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi
echo "✅ Dockerfile exists"

# Check 5: docker-compose.yml exists
echo "[5/6] Checking docker-compose.yml..."
if [ ! -f docker-compose.yml ]; then
    echo "❌ docker-compose.yml not found"
    exit 1
fi
echo "✅ docker-compose.yml exists"

# Validate docker-compose syntax
if ! docker-compose config > /dev/null 2>&1; then
    echo "❌ docker-compose.yml has syntax errors"
    docker-compose config
    exit 1
fi
echo "✅ docker-compose.yml is valid"

# Check 6: Required files exist
echo "[6/6] Checking required application files..."
required_files=("streamlit_app.py" "agents.py" "tasks.py" "rag_service.py" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file not found"
        exit 1
    fi
done
echo "✅ All required files present"

echo ""
echo "=========================================="
echo "✅ All checks passed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Update .env with your API keys"
echo "2. Run: docker-compose build"
echo "3. Run: docker-compose up -d"
echo "4. Access app at: http://localhost:8501"
echo ""
