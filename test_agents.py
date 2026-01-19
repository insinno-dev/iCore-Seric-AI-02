"""
Test script to demonstrate the multiagent device support flow
"""
import os
from dotenv import load_dotenv
from crewai import Crew
from agents import create_device_agent, create_problem_solver_agent, create_rag_query_tool
from tasks import create_device_identification_task, create_problem_narrowing_task, create_solution_recommendation_task
from rag_service import RAGService
from config import config


def test_device_support():
    """Test the device support multiagent flow"""
    
    # Load environment variables
    load_dotenv()
    
    # Verify configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        raise ValueError(error_msg)
    
    print("="*60)
    print("Device Support Service - Agent Test")
    print("="*60 + "\n")
    
    # Initialize RAG Service (optional)
    print("Initializing RAG Service...")
    rag_service = None
    try:
        rag_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "device_solutions")
        
        rag_service = RAGService(
            qdrant_url=rag_url,
            collection_name=collection_name,
            api_key=qdrant_api_key
        )
        rag_service.add_sample_solutions()
        stats = rag_service.get_collection_stats()
        print(f"✓ RAG Service initialized. Collection stats: {stats}\n")
    except Exception as e:
        print(f"⚠ RAG Service not available: {str(e)[:100]}...\n")
        rag_service = None
    
    # Create agents
    print("Creating agents...")
    device_agent = create_device_agent(rag_service)
    problem_solver_agent = create_problem_solver_agent(rag_service)
    
    # Add RAG tool to problem solver agent
    if rag_service:
        rag_tool = create_rag_query_tool(rag_service)
        problem_solver_agent.tools = [rag_tool]
    
    print("✓ Agents created\n")
    
    # Create tasks
    print("Creating tasks...")
    device_task = create_device_identification_task(device_agent)
    problem_task = create_problem_narrowing_task(
        problem_solver_agent, 
        "User reported a device issue"
    )
    
    print("✓ Tasks created\n")
    
    # Test scenarios
    test_cases = [
        "My laptop won't turn on and there's no power response",
        "The router suddenly stopped showing WiFi networks",
        "My printer is showing offline status and won't print",
    ]
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {i}: {user_input}")
        print(f"{'='*60}\n")
        
        # Create crew for this test
        crew = Crew(
            agents=[device_agent, problem_solver_agent],
            tasks=[device_task, problem_task],
            verbose=True,
        )
        
        try:
            print("🔄 Processing request...\n")
            result = crew.kickoff(inputs={"user_problem": user_input})
            
            print("\n" + "="*60)
            print("Analysis Result:")
            print("="*60)
            print(result[:500] + "..." if len(str(result)) > 500 else result)
            print()
            
        except Exception as e:
            print(f"❌ Error during crew execution: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_device_support()
