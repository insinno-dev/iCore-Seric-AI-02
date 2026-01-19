"""
Task Definitions for Device Support Service Workflow
Sequential workflow: Device Agent -> Symptom Agent -> Problem Solver Agent
"""
from crewai import Task
from agents import create_device_agent, create_symptom_agent, create_problem_solver_agent, SUPPORTED_DEVICES, DEVICE_DESCRIPTIONS


def create_device_identification_task(device_agent) -> Task:
    """
    Task 1: Device Agent - Identify and CONFIRM the device type with user
    """
    device_list = "\n".join([f"  • {d}: {DEVICE_DESCRIPTIONS[d]}" for d in SUPPORTED_DEVICES])
    
    return Task(
        description=f"""IMPORTANT: You MUST identify and CONFIRM the correct device.

Supported Devices:
{device_list}

Your workflow:
1. Ask the user which device they have (show the list above)
2. Wait for their response and identify which device they're describing
3. CONFIRM the device - ask "So you have a [DEVICE NAME]? Is that correct?" and wait for YES/NO
4. Once confirmed, ask them to briefly describe the problem
5. Do NOT proceed until you have explicit confirmation of the device model

Example conversation:
- Agent: "Hello! We support these devices: EH222, TG222, OH111. Which one do you have?"
- User: "I have the EH222"
- Agent: "Great! So you're using an EH222 (Icecube Machine). Is that correct?"
- User: "Yes"
- Agent: "Excellent! Now, what problem are you experiencing with your EH222?"

Be friendly and professional. Confirmation is CRITICAL.""",
        expected_output="Confirmed device model with explicit user verification and initial problem description",
        agent=device_agent,
    )


def create_symptom_gathering_task(symptom_agent, device_context: str) -> Task:
    """
    Task 2: Symptom Agent - Gather detailed problem and symptom information STEP-BY-STEP
    """
    return Task(
        description=f"""The user has reported a device issue. Device information identified:
        {device_context}
        
        Your task is to gather detailed symptom information by asking structured questions ONE AT A TIME.
        
        CRITICAL: You MUST ask questions sequentially and wait for responses:
        
        Step 1: "Could you tell me more about the specific symptoms or error messages you are seeing?"
        Step 2: "When did you first notice this problem?"
        Step 3: "Are there any specific actions that seem to trigger this problem or make it worse or better?"
        Step 4: "Have there been any recent changes to your device, such as software updates or physical modifications?"
        Step 5: "Could you walk me through the exact sequence of events leading up to when the problem occurs?"
        Step 6: "Is this issue intermittent, or does it happen constantly?"
        Step 7: "Are there any other details you think might be relevant to diagnosing this problem?"
        
        IMPORTANT RULES:
        - Ask only ONE question at a time
        - Wait for the user's response before asking the next question
        - Acknowledge their response before proceeding
        - Be empathetic and conversational
        - After all 7 steps, provide a comprehensive summary of the symptoms gathered
        
        This step-by-step approach ensures you gather complete and accurate symptom information.""",
        expected_output="Detailed symptom information and comprehensive problem description",
        agent=symptom_agent,
    )


def create_problem_solver_task(problem_solver_agent, problem_context: str, rag_service=None) -> Task:
    """
    Task 3: Problem Solver Agent - Provide step-by-step repair guidance ONE STEP AT A TIME
    Now WITH RAG knowledge base integration for better solutions
    """
    # Query RAG for relevant solutions
    rag_context = ""
    if rag_service:
        try:
            # Extract device type from problem context
            device_type = "Device"  # Default
            if "Device Information:" in problem_context:
                # Try to extract device info from context
                lines = problem_context.split('\n')
                for line in lines:
                    if "EH222" in line or "TG222" in line or "OH111" in line:
                        if "EH222" in line:
                            device_type = "EH222"
                        elif "TG222" in line:
                            device_type = "TG222"
                        elif "OH111" in line:
                            device_type = "OH111"
                        break
            
            similar_solutions = rag_service.search_solutions(
                device_type=device_type,
                problem_description=problem_context,
                limit=3
            )
            if similar_solutions:
                rag_context = "\n\nRELEVANT SOLUTIONS FROM KNOWLEDGE BASE:\n"
                for i, solution in enumerate(similar_solutions, 1):
                    # Handle both dict and string formats
                    if isinstance(solution, dict):
                        sol_text = solution.get('solution', str(solution))
                    else:
                        sol_text = str(solution)
                    rag_context += f"\n{i}. {sol_text}\n"
        except Exception as e:
            print(f"RAG search failed: {e}")
    
    return Task(
        description=f"""Based on the device information and symptoms identified in previous steps:
        {problem_context}
        {rag_context}
        
        Your task is to guide the user through troubleshooting and repair, ONE STEP AT A TIME.
        
        CRITICAL - Interactive Step-by-Step Approach:
        1. Review any knowledge base solutions above if available
        2. Identify the root cause from the symptoms described
        3. Determine the easiest, safest troubleshooting step to try first
        4. Explain ONLY this ONE step clearly:
           - What they need to do
           - Any precautions or warnings
           - What to expect if it works
        5. Tell them to try it and come back with the result
        6. WAIT for their response
        7. If successful: Celebrate, provide any follow-up maintenance tips, end support
        8. If unsuccessful: Acknowledge, explain why it didn't work, suggest the NEXT step
        9. Repeat step-by-step until problem is resolved
        10. Only suggest escalation to professional repair if truly necessary
        
        IMPORTANT RULES:
        - NEVER present multiple options or steps at once
        - NEVER overwhelm the user with a long list of solutions
        - Ask for feedback after each step before moving forward
        - Be encouraging, supportive, and patient
        - Start with safest and easiest steps, progress to more complex only if needed
        - Use knowledge base solutions when available and relevant
        
        Remember: You are guiding them like a human tech support specialist would - one step, 
        one result, one next step.""",
        expected_output="Clear, step-by-step repair guidance with expected outcomes and precautions",
        agent=problem_solver_agent,
    )


# Legacy function for backwards compatibility
def create_problem_narrowing_task(problem_solver_agent, device_identification_context: str) -> Task:
    """
    Legacy task - use create_symptom_gathering_task instead
    """
    return create_symptom_gathering_task(problem_solver_agent, device_identification_context)
