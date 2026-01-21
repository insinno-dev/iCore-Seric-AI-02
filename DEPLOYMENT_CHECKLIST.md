# ✅ Docker Deployment Checklist

## Pre-Deployment Verification

### Step 1: Environment Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Fill in all required API keys in `.env`:
  - [ ] `OPENAI_API_KEY` (OpenAI API key)
  - [ ] `QDRANT_URL` (Your Qdrant cloud URL)
  - [ ] `QDRANT_API_KEY` (Qdrant authentication)
  - [ ] `VOYAGE_API_KEY` (Voyage AI embedding key)
- [ ] Verify `.env` is NOT tracked by git (should be in .gitignore)

### Step 2: Validate Docker Installation
**Windows:**
```bash
validate-docker.bat
```

**Linux/Mac:**
```bash
bash validate-docker.sh
```

Expected output: ✅ All checks passed!

### Step 3: Files Verification

**Required Files Present:**
- [ ] `Dockerfile` (Multi-stage build, runs streamlit_app.py)
- [ ] `docker-compose.yml` (Streamlit service configuration)
- [ ] `.dockerignore` (Build optimization)
- [ ] `.env.example` (Template for environment variables)
- [ ] `.env` (Actual environment variables with secrets)

**Supporting Documentation:**
- [ ] `DOCKER_GUIDE.md` (Comprehensive deployment guide)
- [ ] `DOCKER_SETUP_COMPLETE.md` (Setup summary)
- [ ] `validate-docker.sh` (Linux/Mac validation)
- [ ] `validate-docker.bat` (Windows validation)

**Application Files:**
- [ ] `streamlit_app.py` (Main Streamlit app)
- [ ] `agents.py` (CrewAI agent definitions)
- [ ] `tasks.py` (Agent task definitions)
- [ ] `rag_service.py` (RAG/Vector DB integration)
- [ ] `requirements.txt` (Python dependencies)

### Step 4: Build Docker Image

```bash
# Build the image
docker-compose build

# Expected output:
# [+] Building X.XXs (XX/XX)
# Successfully tagged <image_name>:latest
```

### Step 5: Start Application

```bash
# Start in detached mode
docker-compose up -d

# Verify container is running
docker-compose ps
# Expected status: Up (healthy) after ~40 seconds
```

### Step 6: Application Health Check

```bash
# Check container logs
docker-compose logs streamlit

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8501
# You can now view your Streamlit app in your browser.
# Network URL: http://<container-ip>:8501
```

### Step 7: Web Interface Test

- [ ] Open browser to `http://localhost:8501`
- [ ] Verify Streamlit UI loads
- [ ] Test device identification agent
- [ ] Test multi-turn conversation flow
- [ ] Verify input field resets after responses

### Step 8: Verify Connectivity

```bash
# Test connection to external services
docker-compose exec streamlit curl -I https://api.openai.com
docker-compose exec streamlit curl -I <your-qdrant-url>
```

Expected: HTTP 200/301 responses (successful connections)

## Deployment Commands

### Local Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f streamlit

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Build without cache
docker-compose build --no-cache

# Start with resource limits
docker-compose up -d

# Monitor health
watch 'docker-compose ps'
```

### Maintenance
```bash
# Clean up unused resources
docker-compose down -v

# Restart failed service
docker-compose restart streamlit

# Rebuild specific service
docker-compose build --no-cache streamlit
docker-compose up -d streamlit
```

## Troubleshooting Checklist

### Application Won't Start
- [ ] Verify all environment variables in `.env`
- [ ] Check Docker logs: `docker-compose logs streamlit`
- [ ] Ensure port 8501 is not in use
- [ ] Verify API keys are valid and not expired

### Health Check Failing
- [ ] Wait 40+ seconds (startup grace period)
- [ ] Check network connectivity: `docker-compose exec streamlit curl http://localhost:8501/_stcore/health`
- [ ] Verify API credentials
- [ ] Check Docker daemon status

### Performance Issues
- [ ] Check container memory: `docker stats`
- [ ] Review API rate limits (OpenAI, Qdrant)
- [ ] Check container logs for errors
- [ ] Increase container memory if needed

### Port Already in Use
```bash
# Free the port
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Post-Deployment Verification

### API Connectivity
- [ ] OpenAI API responds to requests
- [ ] Qdrant vector DB accessible
- [ ] Voyage AI embedding service works
- [ ] All endpoints return expected responses

### Application Functionality
- [ ] Device identification agent responds
- [ ] Symptom gathering agent asks questions sequentially
- [ ] Problem solver agent provides solutions
- [ ] Conversation history persists correctly
- [ ] Input field resets after each response

### Performance Metrics
- [ ] Initial startup: < 60 seconds
- [ ] Health check: Passing
- [ ] Response time: < 10 seconds per query
- [ ] Memory usage: < 2GB during operation

### Security Verification
- [ ] `.env` file not in Git history
- [ ] No API keys in logs
- [ ] HTTPS connections to external services
- [ ] Docker network isolated (`crewai-network`)

## Going to Production

### Before Production Deployment
- [ ] Rotate all API keys
- [ ] Create `.env` from `.env.example` with production keys
- [ ] Test with production data/models
- [ ] Set up monitoring and logging
- [ ] Configure resource limits
- [ ] Plan backup strategy

### Production Configuration
- [ ] Use Docker secrets instead of .env files
- [ ] Enable persistent volumes for logs
- [ ] Configure external logging driver
- [ ] Set up health checks alerts
- [ ] Implement auto-scaling if needed

### Backup and Recovery
- [ ] Document all environment variables
- [ ] Store API keys securely (AWS Secrets Manager, Azure Key Vault)
- [ ] Regular backup of configuration
- [ ] Disaster recovery plan documented

## Container Specifications

| Aspect | Value |
|--------|-------|
| **Image Base** | python:3.13-slim |
| **Image Size** | ~1.2GB |
| **Startup Time** | ~60s (first), ~30s (subsequent) |
| **Memory Usage** | 500MB-2GB |
| **Port** | 8501 (Streamlit) |
| **Network** | crewai-network (bridge) |
| **Restart Policy** | unless-stopped |
| **Health Check** | Every 30s, 40s grace period |

## Support Resources

- **Docker CLI Reference**: `docker-compose --help`
- **Logs**: `docker-compose logs -f streamlit`
- **Container Shell**: `docker-compose exec streamlit /bin/bash`
- **Health Status**: `docker-compose ps`
- **Performance**: `docker stats`

## Sign-Off

- [ ] All checklist items completed
- [ ] Application tested and working
- [ ] Documentation reviewed
- [ ] Ready for deployment

---

**Last Updated**: $(date)  
**Deployment Status**: ✅ Ready for Production
