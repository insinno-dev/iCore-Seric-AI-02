"""
FastAPI service for CrewAI backend
Handles device support requests asynchronously
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Device Support CrewAI API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Service globally
logger.info("Initializing RAG Service...")
rag_service = None

def init_rag_service():
    """Initialize RAG service"""
    global rag_service
    try:
        from rag_service import RAGService
        
        # Get Qdrant configuration from environment
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "device_solutions")
        
        logger.info(f"Connecting to Qdrant at: {qdrant_url}")
        
        rag_service = RAGService(
            qdrant_url=qdrant_url,
            collection_name=collection_name,
            api_key=qdrant_api_key
        )
        logger.info("✓ RAG Service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Service: {e}")
        rag_service = None

# Initialize RAG on startup
@app.on_event("startup")
def startup():
    """Initialize RAG service on app startup"""
    global rag_service
    logger.info("App startup - initializing RAG service")
    try:
        init_rag_service()
    except Exception as e:
        logger.error(f"Failed during startup: {e}")

class DeviceIssueRequest(BaseModel):
    """Request model for device support"""
    user_message: str
    conversation_history: list = []

class DeviceIssueResponse(BaseModel):
    """Response model for device support"""
    response: str
    success: bool

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CrewAI API"}

def process_issue_sync(user_message: str):
    """Synchronous function to process device issue (runs in thread pool)"""
    try:
        from crewai import Crew
        from agents import create_device_agent, create_symptom_agent, create_problem_solver_agent
        from tasks import create_device_identification_task, create_symptom_gathering_task, create_problem_solver_task
        
        print(f"\n{'='*80}")
        print(f"[PROCESSING] Device issue: {user_message[:100]}...")
        print(f"{'='*80}\n")
        logger.info(f"Processing device issue: {user_message[:100]}...")
        
        # Check RAG service
        if not rag_service:
            print("❌ ERROR: RAG Service not initialized!")
            raise ValueError("RAG Service not initialized. Please check Qdrant connection.")
        
        # Create agents
        print("[1/4] Creating agents...")
        device_agent = create_device_agent()
        symptom_agent = create_symptom_agent()
        problem_solver_agent = create_problem_solver_agent()
        print("✓ Agents created\n")
        
        # Create tasks
        print("[2/4] Creating tasks...")
        device_task = create_device_identification_task(device_agent)
        symptom_task = create_symptom_gathering_task(symptom_agent, user_message)
        problem_task = create_problem_solver_task(problem_solver_agent, user_message, rag_service)
        print("✓ Tasks created\n")
        
        # Create and run crew
        print("[3/4] Creating crew...")
        crew = Crew(
            agents=[device_agent, symptom_agent, problem_solver_agent],
            tasks=[device_task, symptom_task, problem_task],
            verbose=True
        )
        print("✓ Crew created\n")
        
        # Execute the crew
        print("[4/4] Executing crew...")
        print(f"{'-'*80}\n")
        result = crew.kickoff(inputs={"user_input": user_message})
        print(f"\n{'-'*80}")
        
        print(f"\n✓ Issue processed successfully")
        print(f"{'='*80}\n")
        logger.info("✓ Issue processed successfully")
        return str(result)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"{'='*80}\n")
        logger.error(f"Error processing issue: {str(e)}")
        raise ValueError(f"Error: {str(e)}")

@app.post("/process-issue", response_model=DeviceIssueResponse)
async def process_device_issue(request: DeviceIssueRequest):
    """
    Process a device support issue using CrewAI
    
    Args:
        request: DeviceIssueRequest with user message and conversation history
        
    Returns:
        DeviceIssueResponse with the agent's response
    """
    try:
        # Run the synchronous processing in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, process_issue_sync, request.user_message)
        
        return DeviceIssueResponse(
            response=result,
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error processing issue: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-knowledge-base")
async def search_knowledge_base(query: str):
    """
    Search the knowledge base for solutions
    
    Args:
        query: Search query string
        
    Returns:
        Search results from the knowledge base
    """
    try:
        if not rag_service:
            raise ValueError("RAG Service not initialized")
        
        logger.info(f"Searching knowledge base for: {query}")
        results = rag_service.search(query)
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error searching knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
