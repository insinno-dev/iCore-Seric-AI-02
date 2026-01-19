"""
Main Device Support Service using CrewAI with RAG
"""
import os
from dotenv import load_dotenv

# Always load environment variables first
load_dotenv()

from crewai import Crew
from agents import create_device_agent, create_symptom_agent, create_problem_solver_agent, create_rag_query_tool
from tasks import create_device_identification_task, create_symptom_gathering_task, create_problem_solver_task
from rag_service import RAGService
from config import config


def main():
    """Main function to run the device support service"""
    
    # Load environment variables
    load_dotenv()
    
    # Verify configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        raise ValueError(error_msg)
    
    # Initialize RAG Service
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
    except ConnectionError as e:
        print(f"❌ RAG Connection Error: {e}")
        print(f"   URL: {os.getenv('QDRANT_URL')}")
        print(f"   Collection: {os.getenv('QDRANT_COLLECTION_NAME')}")
        print("   RAG functionality will be limited.\n")
        rag_service = None
    except Exception as e:
        print(f"⚠ RAG Service initialization failed: {str(e)[:100]}...")
        print("RAG functionality will be limited.\n")
        rag_service = None
    
    # Create 3 agents for sequential workflow
    print("Creating agents...")
    device_agent = create_device_agent(rag_service)
    symptom_agent = create_symptom_agent(rag_service)
    problem_solver_agent = create_problem_solver_agent(rag_service)
    
    # Create 3 sequential tasks
    print("Creating tasks...")
    device_task = create_device_identification_task(device_agent)
    symptom_task = create_symptom_gathering_task(
        symptom_agent, 
        "Device information gathered in previous step"
    )
    solver_task = create_problem_solver_task(
        problem_solver_agent,
        "Problem and symptoms identified in previous steps",
        rag_service=rag_service
    )
    
    # Create crew
    print("Creating crew...")
    crew = Crew(
        agents=[device_agent, symptom_agent, problem_solver_agent],
        tasks=[device_task, symptom_task, solver_task],
        verbose=True,
    )
    
    # Get user input
    print("\n" + "="*60)
    print("Device Support Service - Multi-Agent Support System")
    print("="*60 + "\n")
    
    print("Please describe your device issue:")
    print("(Type 'quit' to exit)\n")
    
    user_input = input("> ")
    
    if user_input.lower() == 'quit':
        print("Thank you for using Device Support Service. Goodbye!")
        return
    
    # Execute crew
    print("\nProcessing your request...\n")
    print("="*60)
    
    try:
        result = crew.kickoff(inputs={"user_problem": user_input})
        
        print("\n" + "="*60)
        print("Device Support Service - Analysis Complete")
        print("="*60)
        print("\nFinal Recommendation:\n")
        print(result)
        
    except Exception as e:
        print(f"Error during crew execution: {e}")
        raise


def setup_qdrant_docker():
    """
    Helper function to provide instructions for setting up Qdrant with Docker
    """
    print("""
To use RAG functionality, you need to have Qdrant running.
You can start Qdrant with Docker using:

docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

Then the RAG service will automatically connect and populate sample data.
    """)


if __name__ == "__main__":
    main()
