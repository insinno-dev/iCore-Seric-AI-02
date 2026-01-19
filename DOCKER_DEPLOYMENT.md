# Docker Deployment Guide

Device Support Service - Complete Docker Deployment Instructions

## Quick Start

### Prerequisites
- Docker (version 20.10+)
- Docker Compose (version 1.29+)
- API Keys configured in `.env` file

### Step 1: Configure Environment Variables

Create or update `.env` file with your credentials:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4

# Voyage AI
VOYAGE_API_KEY=your_voyage_api_key

# Qdrant (optional - use cloud or local)
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=device_solutions
```

### Step 2: Build and Run with Docker Compose

```bash
# Build the Docker image
docker-compose build

# Start all services (app + Qdrant)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Step 3: Access the Application

- **Web UI**: http://localhost:8501
- **Qdrant Dashboard**: http://localhost:6333/dashboard

## Individual Docker Commands

### Build Image

```bash
docker build -t device-support:latest .
```

### Run Container

```bash
docker run -d \
  --name device-support-app \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e VOYAGE_API_KEY=your_key \
  -e QDRANT_URL=http://qdrant:6333 \
  device-support:latest
```

### Push to Container Registry

#### Docker Hub

```bash
docker tag device-support:latest yourusername/device-support:latest
docker push yourusername/device-support:latest
```

#### Azure Container Registry (ACR)

```bash
az acr login --name yourregistry
docker tag device-support:latest yourregistry.azurecr.io/device-support:latest
docker push yourregistry.azurecr.io/device-support:latest
```

## Production Deployment Options

### Option 1: Docker Compose (Single Host)

Best for: Development, small deployments, proof of concept

```bash
docker-compose -f docker-compose.yml up -d
```

### Option 2: Docker Swarm

Best for: Multi-host deployment with high availability

```bash
docker swarm init
docker stack deploy -c docker-compose.yml device-support
```

### Option 3: Kubernetes

Best for: Enterprise-scale deployments

Create `device-support-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: device-support
spec:
  replicas: 3
  selector:
    matchLabels:
      app: device-support
  template:
    metadata:
      labels:
        app: device-support
    spec:
      containers:
      - name: app
        image: device-support:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-api-key
        - name: QDRANT_URL
          value: http://qdrant:6333
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: device-support-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: device-support
```

Deploy:
```bash
kubectl apply -f device-support-deployment.yaml
```

### Option 4: Azure Container Instances (ACI)

```bash
az container create \
  --resource-group myResourceGroup \
  --name device-support-aci \
  --image device-support:latest \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your_key QDRANT_URL=http://qdrant:6333
```

### Option 5: AWS ECS

```bash
aws ecs create-service \
  --cluster device-support \
  --service-name device-support-app \
  --task-definition device-support:1 \
  --desired-count 1 \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...
```

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | OpenAI API key for GPT-4 |
| VOYAGE_API_KEY | Yes | - | Voyage AI API key for embeddings |
| QDRANT_URL | No | http://qdrant:6333 | Qdrant database URL |
| QDRANT_API_KEY | No | - | Qdrant API key if using cloud |
| QDRANT_COLLECTION_NAME | No | device_solutions | Collection name in Qdrant |
| CREWAI_TELEMETRY_OPT_OUT | No | true | Disable CrewAI telemetry |

### Volume Mounts

- `/app`: Application code
- `qdrant_storage`: Qdrant database persistence

### Port Mappings

- `8501`: Streamlit web interface
- `6333`: Qdrant REST API

## Monitoring & Maintenance

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
```

### Health Check

```bash
# Check app health
curl http://localhost:8501/_stcore/health

# Check Qdrant health
curl http://localhost:6333/health
```

### Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

# Prune unused images
docker image prune -a
```

## Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs app

# Verify environment variables
docker-compose config

# Rebuild image
docker-compose build --no-cache
```

### Qdrant connection issues

```bash
# Test connection
docker exec device-support-app curl -v http://qdrant:6333/health

# Check Qdrant logs
docker-compose logs qdrant
```

### Memory issues

Increase Docker memory limit:
```bash
# Edit docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
```

## Production Best Practices

1. **Use secrets management** - Store API keys in Docker secrets or external vault
2. **Set resource limits** - Define memory and CPU limits
3. **Enable logging** - Configure centralized logging (ELK, Splunk, etc.)
4. **Use health checks** - Monitor container health
5. **Implement scaling** - Use orchestration tools for multiple replicas
6. **Regular backups** - Backup Qdrant volumes regularly
7. **Security scanning** - Scan images for vulnerabilities
8. **Version control** - Tag images with version numbers

## Performance Optimization

### Multi-stage Build
The included Dockerfile uses multi-stage building to minimize image size (~800MB)

### Caching
Docker layers are cached automatically. Optimize by:
- Copying requirements.txt first
- Placing frequently changing files last

### Image Size
```bash
# Check image size
docker images device-support

# Minimize using alpine base (if compatible)
# Current: python:3.13-slim (~180MB)
```

## Next Steps

1. Configure `.env` with your API keys
2. Run: `docker-compose up -d`
3. Access: http://localhost:8501
4. Monitor logs: `docker-compose logs -f app`
5. For production, push to container registry and deploy to your platform of choice
