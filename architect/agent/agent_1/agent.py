# ============================================================================
# AGENT TEMPLATE - Multi-Agent System with Cooldown and MCP Tools
# ============================================================================
# This template helps you create your own multi-agent system based on Google ADK
# Follow the comments to customize each section for your specific use case
# ============================================================================

# --- IMPORTS SECTION ---
# These are the libraries we need to make our agent system work

import asyncio  # For handling multiple tasks at once
import os  # For reading environment variables
from contextlib import AsyncExitStack  # For managing async resources
from dotenv import load_dotenv  # For loading .env files
from google.adk.agents.llm_agent import LlmAgent  # Single AI agent
from google.adk.agents.loop_agent import LoopAgent  # Agent that runs multiple times
from google.adk.agents.sequential_agent import SequentialAgent  # Agents that run one after another
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset  # External tools your agents can use
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams  # Tool connection settings
import logging   # For printing debug messages
import nest_asyncio   # For running async code in notebooks
from typing import Optional  # For type hints
from google.genai import types  # Google AI types
import requests  # For making web API calls
from datetime import datetime, timezone, timedelta  # For handling time
from toolbox_core import ToolboxSyncClient  # Toolbox integration
from google.adk.agents.callback_context import CallbackContext  # Info about running agents

# ============================================================================
# CONFIGURATION SECTION - CUSTOMIZE THESE VALUES
# ============================================================================

# Load environment variables from .env file (secrets and URLs go here)
load_dotenv()

# --- COOLDOWN CONFIGURATION ---
# This prevents your agents from being called too often (like rate limiting)
# TODO: Set how many seconds to wait between agent runs
COOLDOWN_PERIOD_SECONDS = 60  # Change this number (60 = 1 minute wait)

# TODO: Set your cooldown API URL - this tracks when agents were last used
# Put this URL in your .env file as API_SERVER_URL=http://your-server.com
COOLDOWN_API_URL = os.environ.get("API_SERVER_URL")  # Gets URL from .env file
print(f"COOLDOWN_API_URL: {COOLDOWN_API_URL}")  # Shows what URL we're using

# --- TOOL CONFIGURATION ---
# Tools are external services your agents can call (like calculators, databases, etc.)
# TODO: Set your MCP tools server URL - where your tools live
FUNCTION_TOOLS_URL = os.environ.get("FUNCTION_TOOLS_URL")  # Gets from .env file

# TODO: Set your public URL - how others can access your agent
PUBLIC_URL = os.environ.get("PUBLIC_URL")  # Gets from .env file

# Print the URLs so you can see what's configured
print(f"FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")
print(f"PUBLIC_URL: {PUBLIC_URL}")

# --- LOGGING CONFIGURATION ---
# This controls what debug messages get printed
logging.basicConfig(level=logging.INFO)  # INFO level shows important messages
log = logging.getLogger(__name__)  # Creates a logger for this file

# --- GLOBAL VARIABLES ---
# These will hold our main agent and resources, start as None
root_agent: LlmAgent | None = None  # Will hold our main agent
exit_stack: AsyncExitStack | None = None  # Will manage resources

# ============================================================================
# COOLDOWN CALLBACK FUNCTION - PREVENTS OVERUSE OF AGENTS
# ============================================================================

def check_cool_down(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    This function runs before each agent to check if it's been used too recently.
    
    HOW IT WORKS:
    1. Checks external API to see when agent was last used
    2. If too recent, blocks the agent and sends error message
    3. If okay, updates timestamp and lets agent run
    
    HOW TO CUSTOMIZE:
    - Change COOLDOWN_PERIOD_SECONDS at the top for different wait times
    - Modify the error message text below
    - Add your own checking logic if needed
    
    Args:
        callback_context: Info about which agent is trying to run
        
    Returns:
        None = let agent run, Content = block agent with this message
    """
    # Get the name of the agent that's trying to run
    agent_name = callback_context.agent_name
    print(f"[Callback] Before '{agent_name}': Checking cooldown status...")

    # --- 1. CHECK the Cooldown API ---
    # Ask external service when this agent was last used
    try:
        # Make web request to check last usage time
        response = requests.get(f"{COOLDOWN_API_URL}/cooldown/{agent_name}")
        response.raise_for_status()  # Throw error if request failed
        data = response.json()  # Parse JSON response
        last_used_str = data.get("time")  # Get the timestamp
    except requests.exceptions.RequestException as e:
        # If API is down, print error but let agent run anyway
        print(f"[Callback] ERROR: Could not reach Cooldown API. Allowing agent to run. Reason: {e}")
        return None  # None means "let the agent run"

    # --- 2. EVALUATE the Cooldown Status ---
    # Check if enough time has passed since last use
    if last_used_str:  # If we have a last-used timestamp
        # Convert string timestamp to datetime object
        last_used_time = datetime.fromisoformat(last_used_str)
        # Calculate how much time has passed
        time_since_last_use = datetime.now(timezone.utc) - last_used_time

        # If not enough time has passed, block the agent
        if time_since_last_use < timedelta(seconds=COOLDOWN_PERIOD_SECONDS):
            # Calculate how many seconds left to wait
            seconds_remaining = int(COOLDOWN_PERIOD_SECONDS - time_since_last_use.total_seconds())
            
            # TODO: Customize this message for your agent's personality
            override_message = (
                f"The {agent_name} is on cooldown and cannot be used right now. "
                f"Please wait {seconds_remaining} seconds before trying again."
            )
            print(f"[Callback] Cooldown active for '{agent_name}'. Terminating with message.")
            # Return a message to user instead of running agent
            return types.Content(parts=[types.Part(text=override_message)])

    # --- 3. UPDATE the Cooldown API ---
    # If we get here, agent is allowed to run, so record the current time
    current_time_iso = datetime.now(timezone.utc).isoformat()  # Get current time as string
    payload = {"timestamp": current_time_iso}  # Package as JSON
    
    print(f"[Callback] '{agent_name}' is available. Updating timestamp via Cooldown API...")
    try:
        # Send current time to API to record this usage
        requests.post(f"{COOLDOWN_API_URL}/cooldown/{agent_name}", json=payload)
    except requests.exceptions.RequestException as e:
        # If update fails, print error but still let agent run
        print(f"[Callback] ERROR: Could not update timestamp, but allowing agent to run. Reason: {e}")

    # --- 4. ALLOW the agent to run ---
    print(f"[Callback] Check complete for '{agent_name}'. Proceeding with execution.")
    return None  # None means "proceed with agent execution"

# ============================================================================
# TOOL SETUP - EXTERNAL FUNCTIONS YOUR AGENTS CAN USE
# ============================================================================

# TODO: Replace with your own tools setup
# MCP (Model Context Protocol) lets agents call external functions
toolFunction = MCPToolset(
    # Connection settings for your tools server
    connection_params=SseServerParams(
        url=FUNCTION_TOOLS_URL,  # Where your tools server is running
        headers={}  # Any special headers needed (usually empty)
    )
)

# TODO: Add more tools if you need them
# Example of adding another toolset:
# database_tools = MCPToolset(
#     connection_params=SseServerParams(url=DATABASE_TOOLS_URL, headers={})
# )

# ============================================================================
# AGENT DEFINITIONS - THE AI WORKERS THAT DO YOUR TASKS
# ============================================================================

# --- FIRST AGENT - THE PRIMARY WORKER ---
# TODO: Replace this entire agent with your own
first_agent = LlmAgent(
    # TODO: Pick your AI model (options: gemini-2.5-flash, gpt-4, claude-3, etc.)
    model='gemini-2.5-flash',
    
    # TODO: Give your agent a clear, descriptive name (no spaces)
    name='first_agent',  # This name appears in logs and API calls
    
    # TODO: Write detailed instructions for what this agent should do
    instruction="""
        REPLACE THIS ENTIRE INSTRUCTION BLOCK WITH YOUR AGENT'S JOB
        
        Be very specific about:
        - What task should this agent perform?
        - What input will it receive?
        - Which tools should it use and how?
        - What output should it produce?
        - Any rules or constraints?
        
        Example (DELETE THIS AND WRITE YOUR OWN):
        You are a data processor. Your job is to:
        1. Take the input data provided by the user
        2. Clean and validate the data
        3. Use the 'process_data' tool with the cleaned data
        4. Return only the tool's output, no additional text
    """,
    
    # TODO: List which tools this agent can use (remove if no tools needed)
    tools=[toolFunction]  # This agent can use the tools we set up above
)

# --- SECOND AGENT - THE ANALYZER/PROCESSOR ---
# TODO: Replace this entire agent with your own
second_agent = LlmAgent(
    # TODO: Pick your AI model (can be different from first agent)
    model='gemini-2.5-flash',
    
    # TODO: Give this agent its own descriptive name
    name='second_agent',
    
    # TODO: Write instructions for what this agent does with the first agent's output
    instruction="""
        REPLACE THIS ENTIRE INSTRUCTION BLOCK WITH YOUR AGENT'S JOB
        
        This agent typically:
        - Takes output from the first agent
        - Analyzes, formats, or validates it
        - Applies business logic
        - Prepares final response for user
        
        Example (DELETE THIS AND WRITE YOUR OWN):
        You are a results analyzer. Your job is to:
        1. Take the processed data from the previous step
        2. Generate insights and summaries
        3. Format the results in a user-friendly way
        4. Provide actionable recommendations
    """,
    
    # TODO: If this agent's output should be saved with a specific name, set output_key
    output_key="final_result"  # This saves the agent's response under this name
    # NOTE: Remove output_key line if you don't need to save this agent's output
)

# TODO: Add more agents if your workflow needs them
# Example of a third agent:
# validation_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='validator',
#     instruction="You validate and quality-check the final results...",
#     tools=[toolFunction]  # Only include if this agent needs tools
# )

# ============================================================================
# ROOT AGENT - THE ORCHESTRATOR THAT MANAGES ALL OTHER AGENTS
# ============================================================================

# TODO: Choose your orchestration pattern and customize
# LoopAgent runs agents multiple times in a loop
root_agent = LoopAgent(
    # TODO: Name your overall system (this appears in API and logs)
    name="your_agent_system_name",  # Change to describe your system's purpose
    
    # TODO: List all agents in the order they should run
    sub_agents=[
        first_agent,    # Runs first each iteration
        second_agent    # Runs second each iteration
        # Add more agents here if needed
    ],
    
    # TODO: Set how many times the loop should run
    max_iterations=2,  # 2 means: run all agents, then run them again
    
    # TODO: Describe what your complete system accomplishes
    description="Describe what your multi-agent system does end-to-end.",
    
    # TODO: Add callbacks (functions that run before/after agents)
    before_agent_callback=check_cool_down  # Runs cooldown check before each agent
    # NOTE: Remove this line if you don't want cooldown checking
)

# ============================================================================
# ALTERNATIVE ORCHESTRATION PATTERNS - UNCOMMENT TO USE
# ============================================================================

# TODO: Use SequentialAgent if you want each agent to run only once, in order
# root_agent = SequentialAgent(
#     name="your_sequential_system",
#     sub_agents=[first_agent, second_agent],  # Each runs once, in order
#     description="Runs agents in sequence, each exactly once.",
#     before_agent_callback=check_cool_down  # Optional cooldown
# )

# TODO: Use single LlmAgent if you only need one AI agent
# root_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='single_agent_system',
#     instruction="Complete instructions for your single agent...",
#     tools=[toolFunction],  # Optional tools
#     before_agent_callback=check_cool_down  # Optional cooldown
# )

# ============================================================================
# SERVER SETUP - TURNS YOUR AGENT INTO A WEB API
# ============================================================================

# Import the converter that turns agents into web APIs
from agent_to_a2a import to_a2a

# This runs when you start the script directly (not when importing it)
if __name__ == "__main__":
    import uvicorn  # Web server for Python
    
    # TODO: Customize server settings
    PORT = 8080  # Change if you need a different port number
    HOST = '0.0.0.0'  # '0.0.0.0' means accept connections from anywhere
    
    # Convert your agent system into a web API
    a2a_app = to_a2a(
        root_agent,     # The main agent system we built above
        port=PORT,      # Port number for the API
        public_url=PUBLIC_URL  # Public URL from environment variables
    )
    
    # Start the web server
    uvicorn.run(a2a_app, host=HOST, port=PORT)
    # After this runs, your agents will be available as a web API

# ============================================================================
# ENVIRONMENT VARIABLES NEEDED (.env file)
# ============================================================================
"""
Create a file called '.env' in the same folder as this script.
Put these variables in it (replace the URLs with your actual URLs):

# Optional: API server for tracking agent usage (prevents spam)
API_SERVER_URL=http://your-cooldown-server.com

# Required if using tools: Where your external tools/functions are hosted
FUNCTION_TOOLS_URL=http://your-tools-server.com

# Required for external access: Public URL where people can reach your agent
PUBLIC_URL=http://your-agent-domain.com

# Add any other secrets or URLs your specific agents need:
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
# API_KEY=your-secret-api-key-here
# OPENAI_API_KEY=sk-your-openai-key-here
"""

# ============================================================================
# STEP-BY-STEP CUSTOMIZATION CHECKLIST
# ============================================================================
"""
TO MAKE THIS TEMPLATE WORK FOR YOUR USE CASE:

□ 1. BASIC SETUP
   - Create .env file with your URLs and secrets
   - Set COOLDOWN_PERIOD_SECONDS to your preferred wait time
   - Test that the script runs without errors

□ 2. REPLACE THE AGENTS
   - Change first_agent name and instructions for your primary task
   - Change second_agent name and instructions for your secondary task  
   - Add more agents if your workflow needs them
   - Remove agents you don't need

□ 3. CONFIGURE TOOLS (if needed)
   - Set up your MCP tools server
   - Update FUNCTION_TOOLS_URL in .env
   - Assign tools to the agents that need them
   - Test tool connections

□ 4. CHOOSE ORCHESTRATION
   - Keep LoopAgent if you want agents to run multiple times
   - Use SequentialAgent if agents should run once each, in order
   - Use single LlmAgent if you only need one agent

□ 5. CUSTOMIZE BEHAVIOR
   - Modify cooldown messages and timing
   - Add error handling for your specific use cases
   - Adjust logging levels if needed

□ 6. DEPLOYMENT
   - Set PORT and HOST for your environment
   - Configure PUBLIC_URL for external access
   - Test the complete system end-to-end

□ 7. TESTING CHECKLIST
   - Test each agent individually
   - Test agent-to-agent communication
   - Test cooldown functionality (try calling agents too quickly)
   - Test tool integrations
   - Test with real user input
"""

# ============================================================================
# COMPLETE EXAMPLE - WEATHER REPORTING SYSTEM
# ============================================================================
"""
Here's a complete example of how to fill out this template for a weather reporting system:

# 1. CONFIGURATION (top of file)
COOLDOWN_PERIOD_SECONDS = 30  # 30 second cooldown

# 2. FIRST AGENT - Weather Data Collector
weather_collector = LlmAgent(
    model='gemini-2.5-flash',
    name='weather_collector',
    instruction=\"\"\"
        You are a weather data collector. Your job is to:
        1. Take the city name provided by the user
        2. Use the 'get_weather_data' tool to fetch current weather
        3. Return only the raw weather data from the tool
        4. Do not add any formatting or commentary
    \"\"\",
    tools=[weather_tools]
)

# 3. SECOND AGENT - Weather Report Generator  
weather_reporter = LlmAgent(
    model='gemini-2.5-flash',
    name='weather_reporter',
    instruction=\"\"\"
        You are a friendly weather reporter. Your job is to:
        1. Take the raw weather data from the previous step
        2. Create a friendly, conversational weather report
        3. Include temperature, conditions, and a recommendation for what to wear
        4. Keep it under 100 words and make it engaging
    \"\"\",
    output_key="weather_report"
)

# 4. ROOT AGENT - Weather System
root_agent = LoopAgent(
    name="weather_reporting_system",
    sub_agents=[weather_collector, weather_reporter],
    max_iterations=1,  # Run each agent once
    description="Collects weather data and creates friendly weather reports.",
    before_agent_callback=check_cool_down
)

# 5. ENVIRONMENT VARIABLES (.env file)
API_SERVER_URL=http://localhost:3000
FUNCTION_TOOLS_URL=http://weather-tools.example.com
PUBLIC_URL=http://my-weather-bot.example.com

# 6. USAGE
# User sends: "Weather for New York"
# weather_collector gets weather data using tools
# weather_reporter creates: "Good morning! It's a sunny 72°F in New York today with clear skies. Perfect weather for a walk in the park! I'd recommend light clothing and maybe sunglasses. Enjoy your day!"
"""

# ============================================================================
# COMMON USE CASE EXAMPLES
# ============================================================================
"""
OTHER EXAMPLES OF HOW TO USE THIS TEMPLATE:

1. CUSTOMER SUPPORT SYSTEM
   - Agent 1: Analyzes customer inquiry and categorizes it
   - Agent 2: Searches knowledge base for relevant information  
   - Agent 3: Writes personalized response with solution

2. CONTENT CREATION PIPELINE
   - Agent 1: Researches topic and gathers information
   - Agent 2: Creates outline and structure
   - Agent 3: Writes full content with engaging language

3. DATA ANALYSIS WORKFLOW
   - Agent 1: Cleans and validates input data
   - Agent 2: Performs statistical analysis and calculations
   - Agent 3: Generates insights and visualization suggestions

4. E-COMMERCE ASSISTANT
   - Agent 1: Understands product requirements from user query
   - Agent 2: Searches product database and compares options
   - Agent 3: Makes personalized recommendations with reasoning

5. CODE REVIEW SYSTEM
   - Agent 1: Analyzes code for bugs and security issues
   - Agent 2: Checks code style and best practices
   - Agent 3: Generates comprehensive review report with suggestions

Each example would use the same template structure but with different:
- Agent instructions (what each agent does)
- Tools (external APIs/functions they can call)
- Orchestration (how agents work together)
- Output formatting (what users receive)
"""
