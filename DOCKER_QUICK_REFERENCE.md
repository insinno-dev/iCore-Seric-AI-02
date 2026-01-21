# 🐳 DOCKER QUICK REFERENCE CARD

## ONE-TIME SETUP

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your API keys
# OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, VOYAGE_API_KEY

# 3. Build Docker image
docker-compose build

# 4. Start application
docker-compose up -d

# 5. Access at http://localhost:8501
```

---

## DAILY OPERATIONS

| Command | Purpose |
|---------|---------|
| `docker-compose up -d` | Start application |
| `docker-compose down` | Stop application |
| `docker-compose logs -f` | View real-time logs |
| `docker-compose ps` | Check status |
| `docker-compose restart streamlit` | Restart service |
| `docker-compose exec streamlit /bin/bash` | Access container shell |

---

## ESSENTIAL FILES

| File | What to Know |
|------|-------------|
| `Dockerfile` | Container image (read-only, don't edit) |
| `docker-compose.yml` | Service config (one Streamlit service) |
| `.env.example` | Template for environment variables |
| `.env` | Your actual secrets (NEVER commit to Git) |
| `.dockerignore` | Build optimization (read-only) |

---

## QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Port 8501 in use | `docker-compose down -v && docker-compose up -d` |
| Container won't start | `docker-compose logs streamlit` (check logs) |
| Health check failing | Wait 40+ seconds, verify API keys in .env |
| Slow responses | Check OpenAI/Qdrant rate limits |
| "Connection refused" | Ensure all cloud services are accessible |

---

## VALIDATION

```bash
# Windows
validate-docker.bat

# Linux/Mac
bash validate-docker.sh
```

Expected output: ✅ All checks passed!

---

## MONITORING

```bash
# Check container health
docker-compose ps
# Status should be: Up (healthy)

# View resource usage
docker stats

# Check specific health endpoint
docker-compose exec streamlit curl http://localhost:8501/_stcore/health
```

---

## ENVIRONMENT VARIABLES

### Must Have (Edit .env)
- `OPENAI_API_KEY` - Your OpenAI API key
- `QDRANT_URL` - Your Qdrant cloud URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `VOYAGE_API_KEY` - Your Voyage AI key

### Optional (Defaults Provided)
- `QDRANT_COLLECTION_NAME` - Default: insinnoflux-seric
- `MODEL` - Default: gpt-4
- `AGENT_TEMPERATURE` - Default: 0.3

---

## KEY INFO

- **Container**: crewai-streamlit
- **Port**: 8501
- **Network**: crewai-network
- **Base Image**: python:3.13-slim
- **Image Size**: ~1.2GB
- **Startup Time**: ~60s (first), ~30s (after)

---

## DEPLOYMENT

```bash
# Local development
docker-compose up -d

# Cloud deployment
# 1. Push image to registry
# 2. Use Kubernetes or managed container service
# 3. Configure environment variables
# 4. Deploy stack
```

---

## SECURITY

✅ Secrets in .env (not in Git)  
✅ Network isolation (crewai-network)  
✅ No hardcoded credentials  
✅ .env in .gitignore  

⚠️ **For Production**: Use Docker secrets  

---

## LOGS & DEBUGGING

```bash
# Real-time logs
docker-compose logs -f streamlit

# Last 100 lines
docker-compose logs --tail 100 streamlit

# Follow specific service (if multiple)
docker-compose logs -f streamlit

# Save logs to file
docker-compose logs streamlit > logs.txt
```

---

## DOCUMENTATION

- **Quick Start**: This card ⬅️
- **Setup Guide**: DOCKER_SETUP_COMPLETE.md
- **Full Docs**: DOCKER_GUIDE.md
- **Checklist**: DEPLOYMENT_CHECKLIST.md
- **Troubleshooting**: DOCKER_GUIDE.md (section)

---

## VALIDATE BEFORE DEPLOYING

```bash
# Windows
validate-docker.bat

# Linux/Mac
bash validate-docker.sh
```

---

## VERIFY IT'S WORKING

```bash
# Check container is running
docker-compose ps

# Check logs show no errors
docker-compose logs streamlit

# Test the endpoint
curl http://localhost:8501/_stcore/health

# Open browser to
http://localhost:8501
```

---

## PRODUCTION CHECKLIST

- [ ] API keys rotated and set in .env
- [ ] Validation script passes ✅
- [ ] Image built: `docker-compose build`
- [ ] Container running: `docker-compose ps`
- [ ] Health check passing (after 40s)
- [ ] Web UI loads at http://localhost:8501
- [ ] Multi-turn conversation tested
- [ ] No errors in logs

---

## EMERGENCY RESET

```bash
# Stop everything, clean volumes
docker-compose down -v

# Remove image
docker rmi crewai-streamlit

# Clean builder cache
docker builder prune

# Start fresh
docker-compose build
docker-compose up -d
```

---

## RESOURCE LIMITS (Optional)

Edit `docker-compose.yml` to add:
```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '2'
    reservations:
      memory: 1G
      cpus: '1'
```

---

**Ready to deploy?**

1. Run validation script
2. Edit .env
3. `docker-compose build`
4. `docker-compose up -d`
5. Access http://localhost:8501

✅ **That's it!**
