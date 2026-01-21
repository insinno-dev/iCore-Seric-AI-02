"""
Direct Streamlit Integration with CrewAI
Runs CrewAI agents directly in Streamlit for faster responses
"""
import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable CrewAI telemetry
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

from crewai import Crew
from agents import create_device_agent, create_symptom_agent, create_problem_solver_agent
from tasks import create_device_identification_task, create_symptom_gathering_task, create_problem_solver_task
from rag_service import RAGService

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
    
    .message-user {
        background-color: #f0f5fb;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 4px solid #1a3a52;
    }
    
    .message-agent {
        background-color: #f9f9f9;
        padding: 16px 18px;
        border-radius: 6px;
        margin: 12px 0;
        border-left: 4px solid #4CAF50;
    }
    
    .input-section {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #1a3a52;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stage" not in st.session_state:
    st.session_state.stage = "device_identification"

if "input_reset" not in st.session_state:
    st.session_state.input_reset = 0

if "rag_service" not in st.session_state:
    try:
        st.session_state.rag_service = RAGService(
            qdrant_url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            collection_name=os.getenv("QDRANT_COLLECTION_NAME")
        )
        rag_initialized = True
    except Exception as e:
        st.warning(f"⚠️ RAG Service initialization issue: {str(e)}")
        st.session_state.rag_service = None
        rag_initialized = False

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 Device Support")
    st.markdown("""
    Intelligent multiagent AI system for device troubleshooting and support.
    """)
    
    st.markdown("### ✨ Features")
    st.markdown("""
    • **Smart Device Detection** - Identifies your device type
    • **Detailed Diagnosis** - Asks targeted questions
    • **Step-by-Step Solutions** - Guides you through fixes
    • **Knowledge Base** - Powered by extensive device database
    """)
    
    st.markdown("### ✓ System Status")
    if st.session_state.rag_service:
        st.success("✓ RAG Service Connected")
    else:
        st.warning("⚠ RAG Service Unavailable")

# Main header
st.markdown("""
<div style="text-align: center; margin-bottom: 40px; padding-top: 20px;">
    <h1 class="main-header">🤖 Device Support Service</h1>
    <p class="main-subheader">Intelligent AI-Powered Troubleshooting & Solutions</p>
</div>
""", unsafe_allow_html=True)

# Display chat messages
st.markdown('<div class="input-section"><h3>💬 Conversation</h3></div>', unsafe_allow_html=True)

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
        key=f"user_input_{st.session_state.input_reset}"
    )

with col_button:
    send_button = st.button("🚀 Send", use_container_width=True)

if send_button and user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Determine conversation stage
    conversation_count = len([m for m in st.session_state.messages if m["role"] == "user"])
    
    # Process with CrewAI - one agent per turn for proper multi-turn conversation
    with st.spinner("🔧 Analyzing your issue..."):
        try:
            print(f"\n{'='*80}")
            print(f"[STREAMLIT] Turn {conversation_count}: {user_input[:100]}...")
            print(f"{'='*80}\n")
            
            response = None
            
            # Stage 1: Device Identification (first message only)
            if conversation_count == 1:
                print("[STAGE 1/3] Device Identification")
                device_agent = create_device_agent()
                device_task = create_device_identification_task(device_agent)
                
                crew = Crew(
                    agents=[device_agent],
                    tasks=[device_task],
                    verbose=True
                )
                
                print(f"{'-'*80}\n")
                result = crew.kickoff(inputs={"user_input": user_input})
                response = str(result)
                st.session_state.stage = "device_confirmed"
                
            # Stage 2: Symptom Gathering (after device is confirmed)
            elif conversation_count == 2 or st.session_state.get("stage") == "symptoms":
                print("[STAGE 2/3] Symptom Gathering")
                symptom_agent = create_symptom_agent()
                
                # Get conversation context
                conversation_context = "\n".join([
                    f"{m['role'].upper()}: {m['content'][:200]}"
                    for m in st.session_state.messages[:-1]  # Exclude current message
                ])
                
                symptom_task = create_symptom_gathering_task(symptom_agent, conversation_context)
                
                crew = Crew(
                    agents=[symptom_agent],
                    tasks=[symptom_task],
                    verbose=True
                )
                
                print(f"{'-'*80}\n")
                result = crew.kickoff(inputs={"user_input": user_input, "context": conversation_context})
                response = str(result)
                st.session_state.stage = "symptoms_gathered"
                
            # Stage 3: Problem Solving (after symptoms are gathered)
            else:
                print("[STAGE 3/3] Problem Solving")
                problem_solver_agent = create_problem_solver_agent()
                
                # Get full conversation context
                conversation_context = "\n".join([
                    f"{m['role'].upper()}: {m['content'][:300]}"
                    for m in st.session_state.messages[:-1]  # Exclude current message
                ])
                
                problem_task = create_problem_solver_task(
                    problem_solver_agent,
                    conversation_context,
                    st.session_state.rag_service
                )
                
                crew = Crew(
                    agents=[problem_solver_agent],
                    tasks=[problem_task],
                    verbose=True
                )
                
                print(f"{'-'*80}\n")
                result = crew.kickoff(inputs={"user_input": user_input, "context": conversation_context})
                response = str(result)
            
            print(f"\n{'-'*80}")
            print(f"✓ Stage completed successfully")
            print(f"{'='*80}\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            print(f"{'='*80}\n")
            response = f"❌ Error processing request: {str(e)}"
    
    # Add agent response to history
    st.session_state.messages.append({
        "role": "agent",
        "content": response
    })
    
    # Reset input field by incrementing the counter (changes the key)
    st.session_state.input_reset += 1
    
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
