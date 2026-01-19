"""
Interactive chat interface for Device Support Service with CrewAI agents
"""
import os
from dotenv import load_dotenv

# Always load environment variables first
load_dotenv()

from crewai import Crew
from agents import create_device_agent, create_problem_solver_agent, create_rag_query_tool
from tasks import create_device_identification_task, create_problem_narrowing_task, create_solution_recommendation_task
from rag_service import RAGService
from config import config


def run_chat():
    """Run interactive chat conversation with multiagent crew."""
    
    # Load environment
    load_dotenv()
    
    # Verify configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        raise ValueError(error_msg)
    
    # Initialize RAG (optional)
    print("Initializing services...")
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
        print("✓ RAG Service initialized\n")
    except ConnectionError as e:
        print(f"❌ RAG Connection Error: {e}")
        print(f"   URL: {os.getenv('QDRANT_URL')}")
        print(f"   Collection: {os.getenv('QDRANT_COLLECTION_NAME')}")
        print("   Please verify your credentials in .env file\n")
        rag_service = None
    except Exception as e:
        print(f"⚠ RAG Service not available: {str(e)[:80]}...\n")
        rag_service = None
    
    # Create agents
    print("Creating agents...")
    device_agent = create_device_agent(rag_service)
    problem_solver_agent = create_problem_solver_agent(rag_service)
    
    # Add RAG tool if available
    if rag_service:
        rag_tool = create_rag_query_tool(rag_service)
        problem_solver_agent.tools = [rag_tool]
    
    print("✓ Agents ready\n")
    
    # Display welcome message
    print("=" * 70)
    print("🤖 Device Support Chat - Powered by CrewAI")
    print("=" * 70)
    print("\nWelcome! I'm here to help troubleshoot your device issues.")
    print("Describe your problem, and I'll guide you through solutions.")
    print("\nCommands:")
    print("  • Type your device issue or problem description")
    print("  • Type 'quit' or 'exit' to end the conversation")
    print("  • Type 'clear' to start fresh\n")
    
    # Maintain conversation context
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Handle exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n✅ Thank you for using Device Support Chat. Goodbye!")
                break
            
            # Handle clear command
            if user_input.lower() in ['clear', 'reset']:
                conversation_history = []
                print("\n🔄 Conversation cleared. Starting fresh.\n")
                continue
            
            # Skip empty input
            if not user_input:
                print("Please describe your device issue.\n")
                continue
            
            # Add to conversation history
            conversation_history.append(f"User: {user_input}")
            
            # Build context from recent messages
            recent_context = "\n".join(conversation_history[-4:])  # Last 4 messages
            
            print("\n⏳ Processing your request...\n")
            
            # Create dynamic tasks with conversation context
            device_task = create_device_identification_task(device_agent)
            problem_task = create_problem_narrowing_task(
                problem_solver_agent,
                f"Conversation context:\n{recent_context}"
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[device_agent, problem_solver_agent],
                tasks=[device_task, problem_task],
                verbose=False,  # Set to False for cleaner chat experience
            )
            
            try:
                result = crew.kickoff(inputs={"user_problem": user_input})
                
                # Display response
                print("\n" + "=" * 70)
                print("🤖 Assistant Response:")
                print("=" * 70)
                print(f"\n{result}\n")
                
                # Add to history
                conversation_history.append(f"Assistant: {result}")
                
            except Exception as crew_error:
                print(f"\n⚠ Agent processing error: {str(crew_error)[:100]}...")
                print("Please try rephrasing your question.\n")
        
        except KeyboardInterrupt:
            print("\n\n✅ Chat ended. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)[:100]}...")
            print("Please try again.\n")


def main():
    """Main entry point."""
    try:
        run_chat()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file and ensure OPENAI_API_KEY is set.")
    except Exception as e:
        print(f"Fatal Error: {e}")
        raise


if __name__ == "__main__":
    main()
