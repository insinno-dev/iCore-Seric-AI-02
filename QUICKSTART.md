# Device Support Service - Quick Start Guide

## Setup Complete! ✅

Your CrewAI multiagent device support service is ready. Here's how to get started:

### Option 1: Run Without RAG (Quick Test)

The app runs fine without Qdrant - you can test the agent flow immediately:

```powershell
python main.py
```

Then describe a device issue when prompted, e.g.:
- "My laptop won't turn on"
- "Router has no WiFi"
- "Printer is offline"

### Option 2: Use Local Qdrant (Docker)

If you want RAG functionality with a local Qdrant instance:

```powershell
# In another terminal, start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Update .env to use local Qdrant
# Change: QDRANT_URL=http://localhost:6333
# Remove or comment out: QDRANT_API_KEY

# Then run the app
python main.py
```

### Option 3: Fix Qdrant Cloud Connection

If using Qdrant Cloud, verify:

1. **API Key is correct** - Check your Qdrant dashboard
2. **URL is correct** - Should include `/api` if needed
3. **Network access** - Ensure your IP/network can reach Qdrant Cloud

Update your `.env`:
```
QDRANT_URL=https://YOUR_INSTANCE.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your_actual_api_key
QDRANT_COLLECTION_NAME=device_solutions
```

## Project Files

- `main.py` - Entry point
- `agents.py` - Device-Agent and Problem-Solver-Agent definitions
- `tasks.py` - Task workflow definitions
- `rag_service.py` - RAG/Vector database service
- `config.py` - Configuration management
- `.env` - Your environment variables (keep secret!)
- `requirements.txt` - Python dependencies

## Testing Without Qdrant

The agents work independently of RAG. To test the multiagent flow:

```powershell
python main.py
```

Example interaction:
```
Device Support Service - Multi-Agent Support System
============================================================

Please describe your device issue:
(Type 'quit' to exit)

> My laptop keeps overheating and shutting down randomly
```

The Device-Agent will ask questions, then the Problem-Solver-Agent will provide solutions.

## Next Steps

1. Test the agent flow with the app running
2. Add more device types and solutions in `rag_service.py` (method: `add_sample_solutions()`)
3. Customize agent behavior in `agents.py`
4. Extend tasks in `tasks.py`
5. Set up Qdrant Cloud or local Qdrant for full RAG functionality

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: qdrant_client` | Run: `pip install -r requirements.txt` |
| `ValueError: OPENAI_API_KEY not set` | Add `OPENAI_API_KEY` to `.env` |
| Qdrant connection 403 | Check API key and URL in `.env` |
| Qdrant connection refused | Start local Qdrant with Docker |
| Agent timeouts | Increase model temperature or reduce task complexity |

## Support

For CrewAI docs: https://docs.crewai.com
For Qdrant docs: https://qdrant.tech/documentation/
