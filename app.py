"""
Streamlit Web Interface for Device Support Service
A modern chatbot UI for the CrewAI multiagent device support system
"""
import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Disable CrewAI telemetry
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Load environment
load_dotenv()

# API Configuration
CREWAI_API_URL = os.getenv("CREWAI_API_URL", "http://localhost:8000")

def call_crewai_api(user_message: str, conversation_history: list = []) -> dict:
    """
    Call the CrewAI API to process a device issue
    
    Args:
        user_message: The user's message
        conversation_history: Previous messages in the conversation
        
    Returns:
        API response with the agent's response
    """
    try:
        response = requests.post(
            f"{CREWAI_API_URL}/process-issue",
            json={
                "user_message": user_message,
                "conversation_history": conversation_history
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "response": "❌ Unable to connect to CrewAI API. Make sure the API service is running at " + CREWAI_API_URL
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "response": "❌ CrewAI API request timed out. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "response": f"❌ Error communicating with API: {str(e)}"
        }

# Page config
st.set_page_config(
    page_title="Device Support Service",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    }
    
    .main-header {
        text-align: center;
        color: #1a3a52;
        margin-bottom: 10px;
        font-size: 2.8em;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-subheader {
        text-align: center;
        color: #666;
        margin-bottom: 40px;
        font-size: 1.1em;
        font-weight: 400;
        line-height: 1.6;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #1a3a52, transparent);
        margin: 30px 0;
    }
    
    .message-user {
        background-color: #f0f5fb;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 5px solid #1a3a52;
        line-height: 1.5;
    }
    
    .message-user b {
        color: #1a3a52;
        font-weight: 600;
    }
    
    .message-agent {
        background-color: #ffffff;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 5px solid #0d7377;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        line-height: 1.6;
    }
    
    .message-agent b {
        color: #0d7377;
        font-weight: 600;
    }
    
    .sidebar-section {
        padding: 18px;
        margin: 16px 0;
        border-radius: 6px;
        background-color: #f8fafb;
        border: 1px solid #e0e8f0;
    }
    
    .sidebar-section h4 {
        color: #1a3a52;
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.05em;
        font-weight: 600;
    }
    
    .input-section {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e0e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #1a3a52;
    }
    
    .card h3 {
        color: #1a3a52;
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 1.3em;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🤖 Device Support")
    st.markdown("""
    Intelligent multiagent AI system for device troubleshooting and support.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ✨ Features")
    st.markdown("""
    • **Smart Device Detection** - Identifies your device type
    • **Detailed Diagnosis** - Asks targeted questions
    • **Step-by-Step Solutions** - Guides you through fixes
    • **Knowledge Base** - Powered by extensive device database
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ✓ System Status")
    try:
        api_response = requests.get(f"{CREWAI_API_URL}/health", timeout=2)
        if api_response.status_code == 200:
            st.success("✓ API Connected")
        else:
            st.warning("⚠ API Unavailable")
    except:
        st.warning(f"⚠ Cannot reach API at {CREWAI_API_URL}")
    st.markdown('</div>', unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
    <h1 class="main-header">🤖 Device Support Service</h1>
    <p class="main-subheader">Intelligent AI-Powered Troubleshooting & Solutions</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
st.markdown('<div class="card"><h3>💬 Conversation</h3></div>', unsafe_allow_html=True)

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="message-user"><b>👤 You:</b><br/>{message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="message-agent"><b>🤖 Agent:</b><br/>{message["content"]}</div>',
            unsafe_allow_html=True
        )

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
if len(st.session_state.messages) == 0:
    st.markdown("#### 📝 Describe Your Device Issue")
    placeholder_text = "e.g., My laptop won't turn on, Router has no WiFi, Printer is offline..."
else:
    st.markdown("#### 📝 Your Response")
    placeholder_text = "Type your response here..."

col_input, col_button = st.columns([0.85, 0.15])

with col_input:
    user_input = st.text_input(
        "Message",
        placeholder=placeholder_text,
        label_visibility="collapsed",
        key="user_input"
    )

with col_button:
    send_button = st.button("🚀 Send", use_container_width=True)

if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Get conversation history (user messages only to pass to API)
    conversation_history = [msg for msg in st.session_state.messages if msg["role"] == "user"]
    
    # Call API
    with st.spinner("🔄 Analyzing..."):
        response = call_crewai_api(user_input, conversation_history)
    
    # Add agent response to history
    st.session_state.messages.append({
        "role": "agent",
        "content": response.get("response", "Error processing request")
    })
    
    # Rerun to display new messages
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Clear history button
if len(st.session_state.messages) > 0:
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


# Disable CrewAI telemetry to avoid signal handler warnings in Streamlit
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="Device Support Service",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Design Inspired by service-conception.com
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        color: #1a3a52;
        margin-bottom: 10px;
        font-size: 2.8em;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .main-subheader {
        text-align: center;
        color: #666;
        margin-bottom: 40px;
        font-size: 1.1em;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Professional divider */
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #1a3a52, transparent);
        margin: 30px 0;
    }
    
    /* Message Styles */
    .message-user {
        background-color: #f0f5fb;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 5px solid #1a3a52;
        line-height: 1.5;
    }
    
    .message-user b {
        color: #1a3a52;
        font-weight: 600;
    }
    
    .message-agent {
        background-color: #ffffff;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 5px solid #0d7377;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        line-height: 1.6;
    }
    
    .message-agent b {
        color: #0d7377;
        font-weight: 600;
    }
    
    /* Status Boxes */
    .status-box {
        padding: 18px 20px;
        border-radius: 6px;
        margin: 16px 0;
        font-size: 0.95em;
    }
    
    .status-success {
        background-color: #e8f5e9;
        border-left: 5px solid #0d7377;
        color: #1b5e20;
    }
    
    .status-error {
        background-color: #ffebee;
        border-left: 5px solid #d32f2f;
        color: #b71c1c;
    }
    
    .status-info {
        background-color: #e3f2fd;
        border-left: 5px solid #1a3a52;
        color: #0d47a1;
    }
    
    .status-warning {
        background-color: #fff3e0;
        border-left: 5px solid #f57c00;
        color: #e65100;
    }
    
    /* Card Styles */
    .card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #1a3a52;
    }
    
    .card h3 {
        color: #1a3a52;
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 1.3em;
        font-weight: 600;
    }
    
    /* Button Styles */
    .action-button {
        background-color: #1a3a52;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        text-align: center;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .action-button:hover {
        background-color: #0d7377;
        box-shadow: 0 4px 12px rgba(13, 115, 119, 0.3);
    }
    
    .action-button-secondary {
        background-color: #f5f5f5;
        color: #1a3a52;
        border: 2px solid #1a3a52;
    }
    
    .action-button-secondary:hover {
        background-color: #1a3a52;
        color: white;
    }
    
    /* Contact Section */
    .contact-section {
        text-align: center;
        padding: 32px 24px;
        background: linear-gradient(135deg, #f0f5fb 0%, #ffffff 100%);
        border-radius: 8px;
        border: 1px solid #e0e8f0;
        margin: 24px 0;
    }
    
    .contact-section h2 {
        color: #1a3a52;
        margin-top: 0;
        font-size: 1.6em;
        font-weight: 700;
    }
    
    .contact-section p {
        color: #666;
        font-size: 0.95em;
        line-height: 1.6;
        margin: 12px 0;
    }
    
    .phone-button {
        display: inline-block;
        padding: 14px 32px;
        background-color: #0d7377;
        color: white;
        text-decoration: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 1.05em;
        margin-top: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(13, 115, 119, 0.3);
    }
    
    .phone-button:hover {
        background-color: #1a3a52;
        box-shadow: 0 6px 16px rgba(13, 115, 119, 0.4);
    }
    
    /* Progress Indicator */
    .progress-indicator {
        display: flex;
        justify-content: space-between;
        margin: 24px 0;
        gap: 8px;
    }
    
    .progress-step {
        flex: 1;
        padding: 12px;
        text-align: center;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .progress-step.active {
        background-color: #0d7377;
        color: white;
    }
    
    .progress-step.inactive {
        background-color: #e8f5e9;
        color: #1a3a52;
    }
    
    .progress-step.completed {
        background-color: #1a3a52;
        color: white;
    }
    
    /* Form Styles */
    .input-section {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #e0e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .input-section label {
        color: #1a3a52;
        font-weight: 600;
        font-size: 0.95em;
    }
    
    /* Sidebar Styles */
    .sidebar-section {
        padding: 18px;
        margin: 16px 0;
        border-radius: 6px;
        background-color: #f8fafb;
        border: 1px solid #e0e8f0;
    }
    
    .sidebar-section h4 {
        color: #1a3a52;
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.05em;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85em;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e0e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### 🤖 Device Support")
    st.markdown("""
    Intelligent multiagent AI system for device troubleshooting and support.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("### ✨ Features")
    st.markdown("""
    • **Smart Device Detection** - Identifies your device type
    • **Detailed Diagnosis** - Asks targeted questions
    • **Step-by-Step Solutions** - Guides you through fixes
    • **Knowledge Base** - Powered by extensive device database
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    # Check configuration
    is_valid, error_msg = config.validate()
    if not is_valid:
        st.markdown("### ⚠️ Status")
        st.error(f"Configuration Error: {error_msg}")
    else:
        st.markdown("### ✓ System Status")
        st.success("Configuration Valid")
    
    # RAG status
    if "rag_service" in st.session_state:
        if st.session_state.rag_service:
            st.success("✓ Connected to Knowledge Base")
        else:
            st.warning("⚠ Knowledge Base Unavailable")
    else:
        st.info("Initializing...")
    st.markdown('</div>', unsafe_allow_html=True)

# Main header
st.markdown("""
<div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
    <h1 class="main-header">🤖 Device Support Service</h1>
    <p class="main-subheader">Intelligent AI-Powered Troubleshooting & Solutions</p>
    <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "crew" not in st.session_state:
    st.session_state.crew = None

if "rag_service" not in st.session_state:
    st.session_state.rag_service = None

if "agents_ready" not in st.session_state:
    st.session_state.agents_ready = False

if "current_stage" not in st.session_state:
    st.session_state.current_stage = "initial"  # initial -> device_confirmed -> symptoms_gathered -> complete

if "device_confirmed" not in st.session_state:
    st.session_state.device_confirmed = None

if "symptoms_gathered" not in st.session_state:
    st.session_state.symptoms_gathered = None

if "device_agent" not in st.session_state:
    st.session_state.device_agent = None

if "symptom_agent" not in st.session_state:
    st.session_state.symptom_agent = None

if "problem_solver_agent" not in st.session_state:
    st.session_state.problem_solver_agent = None

if "symptom_conversation_history" not in st.session_state:
    st.session_state.symptom_conversation_history = []

if "symptom_questions_count" not in st.session_state:
    st.session_state.symptom_questions_count = 0

if "problem_solving_history" not in st.session_state:
    st.session_state.problem_solving_history = []

if "problem_solving_step" not in st.session_state:
    st.session_state.problem_solving_step = 0

if "awaiting_solution_confirmation" not in st.session_state:
    st.session_state.awaiting_solution_confirmation = False

# Initialize services on first load
if not st.session_state.agents_ready:
    with st.spinner("🔄 Initializing services..."):
        try:
            # Initialize RAG
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
                st.session_state.rag_service = rag_service
            except Exception as e:
                st.warning(f"RAG Service unavailable: {str(e)[:50]}...")
                st.session_state.rag_service = None
            
            # Create 3 agents (store individually for sequential processing)
            st.session_state.device_agent = create_device_agent(st.session_state.rag_service)
            st.session_state.symptom_agent = create_symptom_agent(st.session_state.rag_service)
            st.session_state.problem_solver_agent = create_problem_solver_agent(st.session_state.rag_service)
            
            st.session_state.agents_ready = True
            st.success("✓ Services initialized successfully!")
            
        except Exception as e:
            st.error(f"❌ Error initializing services: {str(e)}")
            st.session_state.agents_ready = False

# Display chat messages
st.markdown("""
<div class="card">
    <h3>💬 Conversation</h3>
</div>
""", unsafe_allow_html=True)

chat_container = st.container()

with chat_container:
    # Show input field at the start if no messages yet
    if len(st.session_state.messages) == 0 and st.session_state.current_stage == "initial":
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("#### 📝 Start Conversation")
        
        user_input = st.chat_input(
            placeholder="Describe your device issue... (Press Ctrl+Enter to send)",
            key="input_start"
        )
        
        col_submit, col_space = st.columns([0.2, 0.8])
        
        with col_submit:
            submit_button = st.button("🚀 Send", use_container_width=True, key="send_start")
        
        should_submit = submit_button or (user_input is not None)
        
        if should_submit and user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            if st.session_state.agents_ready:
                with st.spinner("🔄 Analyzing device type..."):
                    try:
                        device_task = create_device_identification_task(st.session_state.device_agent)
                        device_crew = Crew(
                            agents=[st.session_state.device_agent],
                            tasks=[device_task],
                            verbose=False,
                        )
                        
                        device_result = device_crew.kickoff(
                            inputs={"user_problem": user_input}
                        )
                        
                        st.session_state.messages.append({
                            "role": "agent",
                            "content": str(device_result)
                        })
                        
                        st.session_state.device_confirmed = str(device_result)
                        st.session_state.current_stage = "device_confirmed"
                        st.rerun()
                        
                    except Exception as e:
                        error_msg = f"Error in device identification: {str(e)[:100]}..."
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "agent",
                            "content": f"❌ {error_msg}"
                        })
            else:
                st.error("❌ Services not ready. Please refresh the page.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display existing messages
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(
                f'<div class="message-user"><b>👤 You:</b><br/>{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message-agent"><b>🤖 Agent:</b><br/>{message["content"]}</div>',
                unsafe_allow_html=True
            )
            
            # Show input field after agent response (except for completion stage)
            if st.session_state.current_stage != "complete" and idx == len(st.session_state.messages) - 1:
                st.markdown("---")
                
                # Show solution confirmation buttons during troubleshooting
                if st.session_state.current_stage == "symptoms_gathered" and st.session_state.awaiting_solution_confirmation:
                    st.markdown("""
                    <div style="padding: 20px; background-color: #f0f5fb; border-radius: 6px; border-left: 5px solid #1a3a52; margin: 16px 0;">
                        <h3 style="color: #1a3a52; margin-top: 0;">✅ Did this solution work?</h3>
                        <p style="color: #666; margin-bottom: 16px;">Please confirm if the troubleshooting step resolved your issue.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    
                    with col1:
                        if st.button("✅ YES - Issue is Fixed!", key="solution_yes", use_container_width=True):
                            completion_message = """✅ **Excellent! Your issue is resolved!** 

Thank you for using Device Support Service. We're glad we could help get your device back to working order.

**Need additional assistance?**
If you have other devices or encounter similar issues in the future, our professional support team is always available to help.
"""
                            
                            st.session_state.messages.append({
                                "role": "agent",
                                "content": completion_message
                            })
                            st.session_state.awaiting_solution_confirmation = False
                            st.session_state.current_stage = "complete"
                            st.rerun()
                    
                    with col2:
                        st.write("")
                    
                    with col3:
                        if st.button("❌ NO - Try Next Step", key="solution_no", use_container_width=True):
                            st.session_state.awaiting_solution_confirmation = False
                            st.session_state.messages.append({
                                "role": "agent",
                                "content": "I understand. Happened anything when you tried?"
                            })
                            st.rerun()
                else:
                    # Show input field for normal conversation
                    st.markdown('<div class="input-section">', unsafe_allow_html=True)
                    st.markdown("#### 📝 Your Response")
                    
                    user_input = st.chat_input(
                        placeholder="Type your response here... (Press Ctrl+Enter to send)",
                        key=f"input_{idx}"
                    )
                    
                    col_submit, col_space = st.columns([0.2, 0.8])
                    
                    with col_submit:
                        submit_button = st.button("🚀 Send", use_container_width=True, key=f"send_{idx}")
                    
                    should_submit = submit_button or (user_input is not None)
                    
                    if should_submit and user_input:
                        st.session_state.messages.append({
                            "role": "user",
                            "content": user_input
                        })
                        
                        # STAGE 1: Device Identification
                        if st.session_state.current_stage == "initial" and st.session_state.agents_ready:
                            with st.spinner("🔄 Analyzing device type..."):
                                try:
                                    device_task = create_device_identification_task(st.session_state.device_agent)
                                    device_crew = Crew(
                                        agents=[st.session_state.device_agent],
                                        tasks=[device_task],
                                        verbose=False,
                                    )
                                    
                                    device_result = device_crew.kickoff(
                                        inputs={"user_problem": user_input}
                                    )
                                    
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": str(device_result)
                                    })
                                    
                                    st.session_state.device_confirmed = str(device_result)
                                    st.session_state.current_stage = "device_confirmed"
                                    st.rerun()
                                    
                                except Exception as e:
                                    error_msg = f"Error in device identification: {str(e)[:100]}..."
                                    st.error(error_msg)
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": f"❌ {error_msg}"
                                    })
                        
                        # STAGE 2: Symptom Gathering (only after device confirmed)
                        elif st.session_state.current_stage == "device_confirmed" and st.session_state.agents_ready:
                            with st.spinner("🔄 Gathering symptom details..."):
                                try:
                                    conversation_context = "\n".join(st.session_state.symptom_conversation_history)
                                    
                                    symptom_task = create_symptom_gathering_task(
                                        st.session_state.symptom_agent,
                                        f"Device: {st.session_state.device_confirmed}\n\nPrevious conversation:\n{conversation_context}"
                                    )
                                    
                                    symptom_crew = Crew(
                                        agents=[st.session_state.symptom_agent],
                                        tasks=[symptom_task],
                                        verbose=False,
                                    )
                                    
                                    symptom_result = symptom_crew.kickoff(
                                        inputs={
                                            "user_response": user_input,
                                            "device_info": st.session_state.device_confirmed,
                                            "conversation_history": conversation_context
                                        }
                                    )
                                    
                                    symptom_response = str(symptom_result)
                                    
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": symptom_response
                                    })
                                    
                                    st.session_state.symptom_conversation_history.append(f"User: {user_input}")
                                    st.session_state.symptom_conversation_history.append(f"Agent: {symptom_response}")
                                    st.session_state.symptom_questions_count += 1
                                    
                                    symptoms_complete = (
                                        "all symptoms" in symptom_response.lower() or
                                        "ready to troubleshoot" in symptom_response.lower() or
                                        "enough information" in symptom_response.lower() or
                                        "i have all the information" in symptom_response.lower() or
                                        "let me now" in symptom_response.lower() or
                                        "now i'll" in symptom_response.lower() or
                                        "proceeding to" in symptom_response.lower() or
                                        st.session_state.symptom_questions_count >= 5
                                    )
                                    
                                    if symptoms_complete:
                                        st.session_state.symptoms_gathered = "\n".join(st.session_state.symptom_conversation_history)
                                        st.session_state.current_stage = "symptoms_gathered"
                                    
                                    st.rerun()
                                    
                                except Exception as e:
                                    error_msg = f"Error in symptom gathering: {str(e)[:100]}..."
                                    st.error(error_msg)
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": f"❌ {error_msg}"
                                    })
                        
                        # STAGE 3: Problem Solving (only after symptoms gathered)
                        elif st.session_state.current_stage == "symptoms_gathered" and st.session_state.agents_ready:
                            with st.spinner("🔄 Analyzing solutions..."):
                                try:
                                    solving_history = "\n".join(st.session_state.problem_solving_history)
                                    
                                    problem_context = f"""
Device Information: {st.session_state.device_confirmed}

Symptoms Gathered: {st.session_state.symptoms_gathered}

Previous troubleshooting steps:
{solving_history}

Current step number: {st.session_state.problem_solving_step}
"""
                                    
                                    solver_task = create_problem_solver_task(
                                        st.session_state.problem_solver_agent,
                                        problem_context,
                                        rag_service=st.session_state.rag_service
                                    )
                                    
                                    solver_crew = Crew(
                                        agents=[st.session_state.problem_solver_agent],
                                        tasks=[solver_task],
                                        verbose=False,
                                    )
                                    
                                    solver_result = solver_crew.kickoff(
                                        inputs={
                                            "user_response": user_input,
                                            "device_info": st.session_state.device_confirmed,
                                            "symptoms": st.session_state.symptoms_gathered,
                                            "solving_history": solving_history
                                        }
                                    )
                                    
                                    solver_response = str(solver_result)
                                    
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": solver_response
                                    })
                                    
                                    st.session_state.problem_solving_history.append(f"User: {user_input}")
                                    st.session_state.problem_solving_history.append(f"Agent: {solver_response}")
                                    st.session_state.problem_solving_step += 1
                                    
                                    st.session_state.awaiting_solution_confirmation = True
                                    
                                    st.rerun()
                                    
                                except Exception as e:
                                    error_msg = f"Error in problem solving: {str(e)[:100]}..."
                                    st.error(error_msg)
                                    st.session_state.messages.append({
                                        "role": "agent",
                                        "content": f"❌ {error_msg}"
                                    })
                        
                        else:
                            st.error("❌ Services not ready. Please refresh the page.")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# Show professional support contact section when chat is complete
if st.session_state.current_stage == "complete":
    st.markdown("""
    <div class="contact-section">
        <h2>📞 Professional Support Available</h2>
        <p>Your issue has been resolved through our AI support system.</p>
        <p>For more complex issues or hands-on assistance, our professional support team is ready to help.</p>
        <a href="tel:+18003348243" class="phone-button">📞 Call Professional Support: +1-800-334-8243</a>
        <p style="margin-top: 16px; font-size: 0.9em; color: #999;">Available 24/7 • Average wait: Less than 2 minutes</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
.footer {
    text-align: center;
    color: #999;
    padding: 20px;
    font-size: 0.85em;
    border-top: 1px solid #eee;
    margin-top: 40px;
}
</style>
<div class="footer">
    <p>Device Support Service • Powered by CrewAI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
