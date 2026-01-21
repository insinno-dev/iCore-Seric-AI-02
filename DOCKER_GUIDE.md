# Docker Deployment Guide

## Overview

This application uses Docker to containerize the Streamlit-based Device Support System with direct CrewAI integration (no separate API layer for performance).

## Quick Start

### 1. Prepare Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:
```
OPENAI_API_KEY=your-key-here
QDRANT_API_KEY=your-key-here
VOYAGE_API_KEY=your-key-here
QDRANT_URL=your-qdrant-url-here
```

### 2. Build and Run

```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f streamlit
```

The application will be available at: **http://localhost:8501**

### 3. Stop the Application

```bash
docker-compose down
```

## File Descriptions

### Dockerfile
- **Multi-stage build** for optimized image size
- Python 3.13-slim base image
- Installs dependencies in builder stage, copies only necessary files to runtime stage
- Runs Streamlit on port 8501
- Health checks enabled

### docker-compose.yml
- **Streamlit service**: Direct CrewAI integration (no API)
- Environment variables from `.env` file
- Volume mount for live development
- Health checks with 40-second startup grace period
- Network isolation via `crewai-network`

### .dockerignore
- Optimizes Docker build context
- Excludes: `__pycache__`, `.venv`, `.git`, `.env`, test files
- Reduces image size and build time

### .env.example
- Template for required environment variables
- Copy to `.env` and fill in actual values
- **IMPORTANT**: `.env` should NEVER be committed to Git

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | sk-proj-... |
| `QDRANT_URL` | Qdrant database URL | https://...eu-central-1-0.aws.cloud.qdrant.io |
| `QDRANT_API_KEY` | Qdrant API key (required) | ... |
| `QDRANT_COLLECTION_NAME` | Vector collection name | insinnoflux-seric |
| `VOYAGE_API_KEY` | Voyage AI embedding key | ... |
| `MODEL` | OpenAI model to use | gpt-4 |
| `AGENT_TEMPERATURE` | Agent reasoning temperature | 0.3 |

## Deployment Scenarios

### Development (Local)

```bash
docker-compose up -d
# App at http://localhost:8501
# Logs: docker-compose logs -f streamlit
```

### Production

Use environment-specific overrides:

```bash
# Create docker-compose.override.yml
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

**Production best practices:**
- Use Docker secrets for sensitive values (not .env files)
- Set resource limits (memory, CPU)
- Configure proper logging drivers
- Use health checks with longer timeouts
- Consider multi-container orchestration (Kubernetes)

## Docker Secrets (Production)

Instead of `.env` files, use Docker secrets:

```bash
# Create secrets
echo "sk-proj-..." | docker secret create openai_api_key -
echo "api-key" | docker secret create qdrant_api_key -

# Update docker-compose.yml to reference secrets
# service:
#   secrets:
#     - openai_api_key
#     - qdrant_api_key
```

In application code:
```python
import os
api_key = open('/run/secrets/openai_api_key').read().strip()
```

## Troubleshooting

### Port Already in Use
```bash
# Check what's using port 8501
netstat -tulpn | grep 8501

# Kill the process
docker-compose down -v
```

### Service Won't Start
```bash
# Check logs
docker-compose logs streamlit

# Verify environment variables
docker-compose config
```

### Slow Performance
1. Check API rate limits (OpenAI, Voyage AI)
2. Monitor Qdrant response times
3. Increase container memory: `docker-compose.yml` -> `services.streamlit.deploy.resources`

### Health Check Failing
- **Initial startup**: First startup takes 40+ seconds (set by `start_period`)
- **API keys invalid**: Verify `.env` values
- **Network issues**: Check Qdrant URL and connectivity

## Cleanup

```bash
# Stop services
docker-compose down

# Remove containers and volumes
docker-compose down -v

# Remove images
docker image rm crewai-streamlit

# Clean builder cache
docker builder prune
```

## Performance Optimization

### Image Size
- Current: ~1.2GB (Python 3.13-slim + dependencies)
- Multi-stage build reduces from ~2.5GB builder stage

### Startup Time
- First run: ~60 seconds (health check grace period)
- Subsequent runs: ~30 seconds

### Runtime Memory
- Base: ~500MB
- With heavy CrewAI reasoning: ~1-2GB

## Security Considerations

⚠️ **CRITICAL**: Never commit `.env` files with API keys

- Use `.gitignore`: `.env` is already ignored
- Use `.env.example` as template
- Rotate keys if accidentally exposed
- Use Docker secrets in production
- Enable API key scoping (limit Qdrant access to specific collections)

## Network Architecture

```
┌─────────────────────────────────────┐
│      User Browser (Port 8501)        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   crewai-network (Docker Network)   │
│  ┌────────────────────────────────┐ │
│  │  Streamlit Service (8501)      │ │
│  │  - CrewAI Agents               │ │
│  │  - RAG Service                 │ │
│  │  - OpenAI/Qdrant Clients       │ │
│  └────────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
   OpenAI  Qdrant  VoyageAI
  (Cloud)  (Cloud)  (Cloud)
```

## Useful Commands

```bash
# View running containers
docker-compose ps

# Access container shell
docker-compose exec streamlit /bin/bash

# Rebuild without cache
docker-compose build --no-cache

# Stream logs
docker-compose logs -f streamlit

# Run single service
docker-compose up streamlit

# Check service health
docker-compose exec streamlit curl http://localhost:8501/_stcore/health

# Stop specific service
docker-compose stop streamlit

# Restart service
docker-compose restart streamlit

# Remove orphan containers
docker-compose down --remove-orphans
```

## Next Steps

1. **Build and test locally**: `docker-compose build && docker-compose up`
2. **Verify health checks**: `docker-compose ps` (should show "healthy")
3. **Push to registry**: `docker tag crewai-streamlit:latest myrepo/crewai-streamlit:latest`
4. **Deploy to cloud**: Use Docker compose or Kubernetes manifests

---

**Questions?** Check logs: `docker-compose logs -f streamlit`
