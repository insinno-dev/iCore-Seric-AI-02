# Device Support Service - MultiAgent CrewAI Application

A sophisticated multi-agent system for device support that uses CrewAI and Qdrant vector database for intelligent problem-solving.

## Features

- **Device-Agent**: Identifies the device type and initial problem
- **Problem-Solver-Agent**: Narrows down issues and provides solutions
- **RAG with Qdrant**: Vector-based semantic search for existing solutions and manuals
- **Multi-Agent Workflow**: Orchestrated communication between agents

## Architecture

```
User Input
    ↓
Device-Agent (Identify Device & Problem)
    ↓
Problem-Solver-Agent (Narrow Issue & Search RAG)
    ↓
Qdrant Vector DB (Search Similar Solutions)
    ↓
Solution & Recommendations
```

## Setup

### Prerequisites

- Python 3.8+
- Docker (for Qdrant)
- OpenAI API key

### Installation

1. **Clone/Create the project**
```bash
cd Test-CrewAI
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo OPENAI_API_KEY=your_api_key_here > .env
```

5. **Start Qdrant (in another terminal)**
```bash
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
```

### Running the Application

```bash
python main.py
```

The system will:
1. Initialize the RAG service and load sample solutions
2. Create two agents: Device-Agent and Problem-Solver-Agent
3. Ask you to describe your device issue
4. Orchestrate multi-agent conversation to diagnose and solve the problem
5. Provide step-by-step solutions with manual references

## Sample Solutions Included

The system comes with sample solutions for:
- **Laptop**: Power issues, display problems
- **Router**: Connection issues, WiFi problems
- **Printer**: Offline status, printing failures

## Project Structure

```
Test-CrewAI/
├── main.py              # Main entry point
├── rag_service.py       # RAG/Vector DB service
├── agents.py            # Agent definitions
├── tasks.py             # Task definitions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md            # This file
```

## Advanced Usage

### Adding Custom Solutions

```python
from rag_service import RAGService

rag_service = RAGService()
rag_service.add_solution(
    device_type="Laptop",
    problem="Battery not charging",
    solution="Check power adapter connection. Replace battery if faulty.",
    manual_reference="Section 4.2 - Battery Troubleshooting"
)
```

### Customizing Agents

Edit `agents.py` to modify:
- Agent roles and goals
- System prompts (backstory)
- Temperature settings (creativity vs consistency)
- Tools available to each agent

### Extending Tasks

Edit `tasks.py` to:
- Add more detailed task descriptions
- Change expected outputs
- Add new tasks to the workflow

## Troubleshooting

### Qdrant Connection Error

Make sure Qdrant is running:
```bash
docker ps  # Should show qdrant container
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant  # If not running
```

### OpenAI API Error

Verify your API key:
```bash
echo $env:OPENAI_API_KEY  # Windows PowerShell
echo $OPENAI_API_KEY      # Linux/Mac
```

### Agent Not Responding

Check that CrewAI is properly installed:
```bash
pip install --upgrade crewai
```

## Future Enhancements

- [ ] Web interface for better UX
- [ ] Integration with ticketing systems
- [ ] Machine learning model for issue classification
- [ ] Multi-language support
- [ ] Email/chat integrations
- [ ] Performance metrics and analytics

## License

Your License Here

## Support

For issues or feature requests, contact: support@example.com
