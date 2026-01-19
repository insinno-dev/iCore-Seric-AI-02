# Device Support Service - Streamlit Web Interface

## Overview

The Streamlit web interface provides a modern, user-friendly chat interface for the Device Support Service multiagent system. It enables human interaction with CrewAI agents for device troubleshooting and problem diagnosis.

## Features

### 🤖 Intelligent Agent System
- **Device-Agent**: Identifies device types and initial problems
- **Problem-Solver-Agent**: Asks targeted follow-up questions to narrow down issues
- **RAG Integration**: Searches knowledge base for solutions

### 💬 Chat Interface
- Clean, responsive chat UI
- Conversation history persistence
- Real-time agent responses
- Clear message formatting with user/agent indicators

### ⚙️ Configuration Management
- Environment variable validation
- RAG service status display
- Configuration sidebar with system information

### 📊 Service Status
- Qdrant Cloud connection validation
- Configuration state verification
- Service health indicators

## Installation

### Prerequisites
- Python 3.13+
- CrewAI 1.8.0
- OpenAI API key
- Qdrant Cloud account with credentials

### Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment** (`.env`):
```env
OPENAI_API_KEY=your_key_here
QDRANT_URL=https://your-instance.eu-central-1-0.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your_api_key_here
QDRANT_COLLECTION_NAME=insinnoflux-seric
```

3. **Run the app**:
```bash
streamlit run app.py
```

## Usage

### Starting the Web Server

```bash
cd /path/to/project
streamlit run app.py
```

The app will be available at:
- **Local**: `http://localhost:8501`
- **Network**: `http://<your-ip>:8501`

### Interacting with the Chatbot

1. **Open the web interface** in your browser
2. **Describe your device issue** in the chat input field
3. **Follow the agent's questions** for targeted diagnosis
4. **Receive solutions** from the knowledge base
5. **Clear conversation** using the clear button to start fresh

### Example Interactions

#### Issue 1: Laptop Won't Turn On
```
User: "My laptop won't turn on anymore"
Agent: [Identifies device as laptop]
Agent: "When you try to power on, what happens? 
        - Do you hear any sounds?
        - Do any lights come on?
        - Is the power adapter working?"
User: "No sounds, no lights, and the adapter has a green light"
Agent: [Narrows down to power delivery issue]
Agent: "Try these solutions:
        1. Force reset (hold power button 30 seconds)
        2. Test with different power outlet
        3. Check battery connection..."
```

#### Issue 2: WiFi Router Problem
```
User: "My WiFi router keeps disconnecting"
Agent: [Identifies device as router]
Agent: "How often does it disconnect?
        - Several times per hour?
        - Once per day?
        - Only during specific activities?"
...
```

#### Issue 3: Printer Offline
```
User: "My printer is offline and not responding"
Agent: [Identifies device as printer]
Agent: "What type of connection?
        - USB cable
        - Network (WiFi/Ethernet)
        - Bluetooth?"
...
```

## Architecture

### Components

```
Streamlit Web Interface (app.py)
    ↓
Session State Management
    ├─ Messages (conversation history)
    ├─ Crew (agent orchestration)
    ├─ RAG Service (vector database)
    └─ Agents (Device-Agent, Problem-Solver-Agent)
    ↓
CrewAI Framework (agents.py, tasks.py)
    ├─ Device-Agent: Initial device identification
    ├─ Problem-Solver-Agent: Issue diagnosis
    └─ Tasks: Workflow orchestration
    ↓
RAG Service (rag_service.py)
    ↓
Qdrant Cloud (Vector Database)
    ├─ Collection: insinnoflux-seric
    └─ Embeddings: OpenAI (1536-dimensional)
    ↓
OpenAI API
    ├─ GPT-4: Agent intelligence
    └─ Text-Embedding-3-Large: Semantic search
```

### Data Flow

1. **User Input** → Streamlit form
2. **Conversation Stored** → Session state
3. **Crew Execution** → CrewAI agents process with RAG tools
4. **Agent Response** → Returned as markdown
5. **Display Update** → Streamlit re-renders conversation

### Session State Management

The app maintains:
- `messages`: List of user/agent messages
- `crew`: CrewAI Crew instance
- `rag_service`: RAG service connection
- `agents_ready`: Initialization flag

This ensures:
- Conversation history persists across interactions
- Agents initialized only once
- RAG service connection reused efficiently

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and embeddings | Yes |
| `QDRANT_URL` | Qdrant Cloud instance URL with port :6333 | Yes |
| `QDRANT_API_KEY` | Qdrant authentication token | Yes |
| `QDRANT_COLLECTION_NAME` | Vector database collection name | No (default: device_solutions) |

### Streamlit Configuration

Optional: Create `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = false

[logger]
level = "error"

[client]
showErrorDetails = false
```

## Performance Considerations

### Optimization Tips

1. **First Load**: 10-15 seconds (service initialization)
2. **Subsequent Messages**: 5-10 seconds (agent processing)
3. **RAG Search**: ~2-3 seconds (Qdrant query + embedding)

### Scaling

For production deployment:
- Use gunicorn/uWSGI with Streamlit
- Implement message pagination for large histories
- Cache embeddings for frequent queries
- Consider dedicated Qdrant cluster

## Troubleshooting

### Issue: "Configuration Error" appears

**Solution**: Verify `.env` file:
```bash
# Check variables are set
cat .env | grep -E "OPENAI|QDRANT"
```

### Issue: "RAG Service Not Available"

**Solution**: Check Qdrant connection:
```bash
python diagnose_qdrant.py
```

### Issue: Messages not being saved

**Solution**: Streamlit session state may have reset. Check:
- Browser cache/cookies
- Console for JavaScript errors
- Server logs for Python errors

### Issue: Agent responses are slow

**Solution**:
1. Check OpenAI API status
2. Monitor Qdrant query performance
3. Verify network connectivity
4. Check for rate limiting

## Testing

### Run Comprehensive Tests

```bash
python test_streamlit_app.py
```

This validates:
- ✓ App syntax
- ✓ Dependencies installed
- ✓ Configuration valid
- ✓ RAG connectivity
- ✓ Agent creation
- ✓ Task creation

### Manual Testing

1. **Test Case 1**: Device identification
   - Input: "My laptop has a problem"
   - Expected: Agent identifies device type

2. **Test Case 2**: RAG search
   - Input: Device issue with known solution
   - Expected: Knowledge base results shown

3. **Test Case 3**: Conversation history
   - Input: Multiple messages
   - Expected: All messages persist in UI

4. **Test Case 4**: Error handling
   - Expected: Graceful degradation if services unavailable

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t device-support-service .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e QDRANT_URL=$QDRANT_URL \
  -e QDRANT_API_KEY=$QDRANT_API_KEY \
  device-support-service
```

### Cloud Deployment

#### Streamlit Cloud
```bash
# Create .streamlit/secrets.toml
OPENAI_API_KEY = "..."
QDRANT_URL = "..."
QDRANT_API_KEY = "..."

# Deploy
streamlit deploy
```

#### AWS/Azure/GCP
Deploy using Docker with above configuration

## API Reference

### Streamlit Components Used

- `st.set_page_config()`: Page configuration
- `st.sidebar`: Configuration sidebar
- `st.form()`: Chat input form
- `st.session_state`: Persistent state
- `st.spinner()`: Loading indicators
- `st.error()`, `st.success()`, `st.warning()`: Status messages
- `st.markdown()`: Rich text formatting

### Integration Points

#### CrewAI Integration
```python
from crewai import Crew
crew = Crew(
    agents=[device_agent, problem_solver_agent],
    tasks=[device_task, problem_task],
    verbose=False
)
result = crew.kickoff(inputs={"user_problem": user_input})
```

#### RAG Integration
```python
from rag_service import RAGService
rag = RAGService(qdrant_url, collection_name, api_key)
solutions = rag.search_solutions(query, top_k=3)
```

## Development

### Project Structure
```
├── app.py                 # Main Streamlit app
├── agents.py             # Agent definitions
├── tasks.py              # Task definitions
├── rag_service.py        # RAG integration
├── config.py             # Configuration management
├── test_streamlit_app.py # Streamlit tests
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

### Contributing

When modifying the Streamlit app:
1. Maintain session state consistency
2. Add error handling for all external calls
3. Keep UI responsive (avoid blocking operations)
4. Test with multiple message types

## License

Device Support Service © 2024

## Support

For issues or questions:
1. Check [troubleshooting section](#troubleshooting)
2. Review test output: `python test_streamlit_app.py`
3. Run diagnostics: `python diagnose_qdrant.py`
