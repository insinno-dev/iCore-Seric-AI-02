"""
Test script for Device Support Chat - Automated test
"""
import os
from dotenv import load_dotenv
from crewai import Crew
from agents import create_device_agent, create_problem_solver_agent, create_rag_query_tool
from tasks import create_device_identification_task, create_problem_narrowing_task
from rag_service import RAGService
from config import config

def test_chat():
    """Test the chat interface with sample inputs."""
    
    # Load environment
    load_dotenv()
    
    # Verify configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        print(f"❌ Configuration Error: {error_msg}")
        return False
    
    # Initialize RAG
    print("=" * 70)
    print("🧪 Testing Device Support Service")
    print("=" * 70)
    print("\n1️⃣ Initializing RAG Service...")
    rag_service = None
    try:
        rag_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "device_solutions")
        
        print(f"   Loading from .env:")
        print(f"   - URL: {rag_url}")
        print(f"   - Collection: {collection_name}")
        print(f"   - API Key: {qdrant_api_key[:20]}...{qdrant_api_key[-5:]}")
        
        rag_service = RAGService(
            qdrant_url=rag_url,
            collection_name=collection_name,
            api_key=qdrant_api_key
        )
        print("   ✓ RAG Service connected successfully!\n")
    except ConnectionError as e:
        print(f"   ❌ RAG Connection Error: {e}")
        print("   ⚠ Continuing without RAG...\n")
        rag_service = None
    except Exception as e:
        print(f"   ⚠ RAG Service error: {e}\n")
        rag_service = None
    
    # Create agents
    print("2️⃣ Creating agents...")
    try:
        device_agent = create_device_agent(rag_service)
        problem_solver_agent = create_problem_solver_agent(rag_service)
        
        if rag_service:
            rag_tool = create_rag_query_tool(rag_service)
            problem_solver_agent.tools = [rag_tool]
        
        print("   ✓ Agents created successfully!\n")
    except Exception as e:
        print(f"   ❌ Error creating agents: {e}")
        return False
    
    # Test conversation
    print("3️⃣ Testing conversation flow...")
    test_inputs = [
        "My laptop won't turn on",
        "Router is not showing WiFi",
        "Printer is offline"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n   Test {i}: '{user_input}'")
        try:
            device_task = create_device_identification_task(device_agent)
            problem_task = create_problem_narrowing_task(problem_solver_agent, f"User: {user_input}")
            
            crew = Crew(
                agents=[device_agent, problem_solver_agent],
                tasks=[device_task, problem_task],
                verbose=False,
            )
            
            result = crew.kickoff(inputs={"user_problem": user_input})
            print(f"   ✓ Response: {str(result)[:100]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}...")
            return False
    
    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_chat()
    exit(0 if success else 1)
