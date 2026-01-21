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
from crewai import Crew
from agents import create_device_agent, create_symptom_agent, create_problem_solver_agent, create_rag_query_tool
from tasks import create_device_identification_task, create_symptom_gathering_task, create_problem_solver_task
from rag_service import RAGService
from config import config

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
try:
    rag_service = RAGService()
    logger.info("✓ RAG Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Service: {e}")
    rag_service = None


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
        logger.info(f"Processing device issue: {request.user_message[:100]}...")
        
        # Verify configuration
        is_valid, error_msg = config.validate()
        if not is_valid:
            raise ValueError(error_msg)
        
        # Create agents
        device_agent = create_device_agent()
        symptom_agent = create_symptom_agent()
        problem_solver_agent = create_problem_solver_agent()
        
        # Create tasks
        device_task = create_device_identification_task(device_agent, request.user_message)
        symptom_task = create_symptom_gathering_task(symptom_agent, request.user_message)
        problem_task = create_problem_solver_task(problem_solver_agent, request.user_message)
        
        # Create and run crew
        crew = Crew(
            agents=[device_agent, symptom_agent, problem_solver_agent],
            tasks=[device_task, symptom_task, problem_task],
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff(inputs={"user_input": request.user_message})
        
        logger.info("✓ Issue processed successfully")
        return DeviceIssueResponse(
            response=str(result),
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
