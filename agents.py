"""
CrewAI Agent Definitions for Device Support Service
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from rag_service import RAGService

# Define supported devices
SUPPORTED_DEVICES = ["EH222", "EH130", "EH330"]
DEVICE_DESCRIPTIONS = {
    "EH222": "EH222 - Ice Cube Machine",
    "EH130": "EH130 - Ice Cube Machine",
    "EH330": "EH330 - Ice Cube Machine"
}


def create_device_agent(rag_service: RAGService = None) -> Agent:
    """
    Create Device Agent that identifies and confirms the device type
    """
    device_list = ", ".join([f"{d} ({DEVICE_DESCRIPTIONS[d]})" for d in SUPPORTED_DEVICES])
    
    return Agent(
        role="Device Support Specialist",
        goal="Identify, confirm, and understand what specific device the user has and what problem they are experiencing",
        backstory=f"""You are an experienced device support specialist. You work with the following supported devices:
        {device_list}
        
        Your job is to:
        1. Ask the user which device they have from the supported list
        2. CONFIRM they selected the correct device (very important!)
        3. Be absolutely certain before moving forward
        
        Supported devices: {', '.join(SUPPORTED_DEVICES)}
        
        IMPORTANT: Always show the device list to users and get explicit confirmation 
        of the correct device model before proceeding. Ask "Is this correct?" and wait for confirmation.
        Be friendly and professional. Ask one question at a time.""",
        llm=ChatOpenAI(model="gpt-4", temperature=0.3),
        verbose=True,
        allow_delegation=False,
    )


def create_symptom_agent(rag_service: RAGService = None) -> Agent:
    """
    Create Problem and Symptom Agent that gathers detailed problem information
    """
    return Agent(
        role="Symptom and Problem Specialist",
        goal="Gather detailed information about the device problem and symptoms by asking step-by-step questions",
        backstory="""You are an experienced technical support specialist who excels at gathering 
        detailed symptom information through structured, step-by-step questioning.
        
        IMPORTANT - You MUST ask questions ONE AT A TIME, waiting for the user's response to each 
        question before asking the next one. Never ask multiple questions in a single response.
        
        Your question sequence:
        1. "Could you tell me more about the specific symptoms or error messages you are seeing?"
        2. "When did you first notice this problem?"
        3. "Are there any specific actions that seem to trigger this problem or make it worse or better?"
        4. "Have there been any recent changes to your device, such as software updates or physical modifications?"
        5. "Could you walk me through the exact sequence of events leading up to when the problem occurs?"
        6. "Is this issue intermittent, or does it happen constantly?"
        7. "Are there any other details you think might be relevant to diagnosing this problem?"
        
        After each user response ask the NEXT question. Be short, crisp 
        and empathetic. Only move to the next question after receiving their answer.
        
        After all 7 questions, summarize all the symptom information you've gathered.""",
        llm=ChatOpenAI(model="gpt-4", temperature=0.3),
        verbose=True,
        allow_delegation=False,
    )


def create_problem_solver_agent(rag_service: RAGService = None) -> Agent:
    """
    Create Problem Solver Agent that provides repair steps and solutions
    """
    return Agent(
        role="Technical Problem Solver",
        goal="Guide the user through repair steps ONE AT A TIME, waiting for feedback before proceeding to the next step",
        backstory="""You are an expert human-like troubleshooter who guides users through fixing problems step-by-step.
        
        IMPORTANT - You guide users through troubleshooting like a real tech support specialist would:
        
        Your step-by-step approach:
        1. Start with the EASIEST troubleshooting step first
        2. Clearly explain that ONE step - what they need to do, why, and any precautions
        3. Tell them to try it and report back
        4. WAIT for their response on whether it worked
        5. If successful - celebrate and end the support session
        6. If NOT successful - DIRECTLY move to the NEXT most appropriate troubleshooting step
        7. Repeat until the problem is solved or escalation is needed
        
        CRITICAL RULES:
        - NEVER provide all solutions at once
        - NEVER list multiple steps for the user to choose from
        - ONLY suggest ONE troubleshooting step at a time
        - Wait for user feedback after each step before proceeding
        - Be encouraging and supportive throughout
        - Explain the reasoning behind each step, but very short
        - Escalate to professional repair only when absolutely necessary
        
        You have access to a comprehensive database of device solutions and troubleshooting guides.""",
        llm=ChatOpenAI(model="gpt-4", temperature=0.3),
        verbose=True,
        allow_delegation=False,
    )


def create_rag_query_tool(rag_service: RAGService):
    """
    Create a simple RAG query tool without decorators
    Returns a callable function that searches the knowledge base
    """
    def search_knowledge_base(device_type: str, problem_description: str) -> str:
        """
        Search the knowledge base for existing solutions
        
        Args:
            device_type: Type of device (e.g., 'Laptop', 'Router')
            problem_description: Detailed description of the problem
            
        Returns:
            Formatted string with relevant solutions from the knowledge base
        """
        if not rag_service:
            return "No RAG service available."
            
        solutions = rag_service.search_solutions(device_type, problem_description, limit=3)
        
        if not solutions:
            return "No matching solutions found in the knowledge base."
        
        result = "Found relevant solutions:\n\n"
        for i, sol in enumerate(solutions, 1):
            result += f"Solution {i} (Relevance: {sol['score']:.2f}):\n"
            result += f"  Problem: {sol['problem']}\n"
            result += f"  Solution: {sol['solution']}\n"
            if sol.get('manual_reference'):
                result += f"  Manual Reference: {sol['manual_reference']}\n"
            result += "\n"
        
        return result
    
    return search_knowledge_base

