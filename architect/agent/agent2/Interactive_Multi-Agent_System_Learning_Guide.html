# ============================================================================
# SEQUENTIAL AGENT TEMPLATE - Simple Multi-Agent Pipeline
# ============================================================================
# This template creates a simple pipeline where agents run one after another
# Perfect for workflows like: Research → Process → Format → Output
# Based on Google ADK framework with MCP tools integration
# ============================================================================

# --- IMPORTS SECTION ---
# These libraries provide the foundation for your agent system

import asyncio  # Handles running multiple tasks at the same time
import os  # Reads environment variables from your system
from contextlib import AsyncExitStack  # Manages cleanup when program ends
from dotenv import load_dotenv  # Loads secrets from .env file
from google.adk.agents.llm_agent import LlmAgent  # Creates individual AI agents
from google.adk.agents.sequential_agent import SequentialAgent  # Runs agents one by one
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset  # External tools/functions
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams  # Tool connection config
import logging   # Prints debug and status messages
import nest_asyncio   # Allows async code to run in Jupyter notebooks
from toolbox_core import ToolboxSyncClient  # Connects to toolbox databases

# ============================================================================
# ENVIRONMENT SETUP - LOADS YOUR CONFIGURATION
# ============================================================================

# Load all variables from .env file (API keys, URLs, secrets)
load_dotenv()
# IMPORTANT: Create a .env file in your project folder with your settings

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)  # INFO shows important messages only
log = logging.getLogger(__name__)  # Creates logger for this specific file

# ============================================================================
# GLOBAL VARIABLES - CONTAINERS FOR YOUR MAIN COMPONENTS
# ============================================================================

# --- Initialize main components as None (will be set up later) ---
root_agent: LlmAgent | None = None  # Will hold your main agent system
exit_stack: AsyncExitStack | None = None  # Will manage cleanup when program exits

# ============================================================================
# CONFIGURATION SECTION - CUSTOMIZE THESE FOR YOUR PROJECT
# ============================================================================

# --- DATABASE AND TOOLS CONFIGURATION ---
# TODO: Set your database tools URL (where stored tools/functions live)
DB_TOOLS_URL = os.environ.get("DB_TOOLS_URL")  # Put this in your .env file

# TODO: Set your function tools URL (where live tools/APIs are hosted)  
FUNCTION_TOOLS_URL = os.environ.get("FUNCTION_TOOLS_URL")  # Put this in your .env file

# TODO: Set your public URL (how users will access your agent)
PUBLIC_URL = os.environ.get("PUBLIC_URL")  # Put this in your .env file

# Print URLs to verify they loaded correctly
print(f"DB_TOOLS_URL: {DB_TOOLS_URL}")
print(f"FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")
print(f"PUBLIC_URL: {PUBLIC_URL}")

# ============================================================================
# TOOL SETUP - CONFIGURE EXTERNAL FUNCTIONS YOUR AGENTS CAN USE
# ============================================================================

# --- DATABASE TOOLSET SETUP ---
# TODO: Replace with your own database tools
# This connects to a toolbox database containing pre-built functions
toolbox = ToolboxSyncClient(DB_TOOLS_URL)  # Connects to your toolbox server

# TODO: Change 'summoner-librarium' to your actual toolset name
toolDB = toolbox.load_toolset('your-toolset-name')  # Loads specific toolset from database
# EXAMPLE TOOLSET NAMES: 'user-management', 'data-processing', 'email-tools'

# --- LIVE FUNCTION TOOLSET SETUP ---
# TODO: Configure your live/external tools server
# This connects to real-time tools like APIs, databases, external services
toolFunction = MCPToolset(
    connection_params=SseServerParams(
        url=FUNCTION_TOOLS_URL,  # Your tools server URL
        headers={}  # Add authentication headers if needed: {"Authorization": "Bearer token"}
    )
)

# TODO: Add more toolsets if you have multiple tool servers
# Example:
# email_tools = MCPToolset(
#     connection_params=SseServerParams(url=EMAIL_TOOLS_URL, headers={})
# )

# ============================================================================
# AGENT DEFINITIONS - CREATE YOUR AI WORKERS
# ============================================================================

# --- FIRST AGENT - PRIMARY DATA COLLECTOR/PROCESSOR ---
# TODO: Replace this with your first agent's specific job
first_agent = LlmAgent(
    # TODO: Choose your AI model (gemini-2.5-flash, gpt-4, claude-3, etc.)
    model='gemini-2.5-flash',
    
    # TODO: Give your agent a descriptive name (appears in logs and API)
    name='data_collector_agent',  # Change to match your agent's purpose
    
    # TODO: Write specific instructions for what this agent should do
    instruction="""
        REPLACE THIS ENTIRE INSTRUCTION WITH YOUR AGENT'S JOB
        
        Your first agent typically:
        - Receives initial user input
        - Gathers information using tools
        - Processes raw data
        - Prepares data for the next agent
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a research assistant. Your job is to:
        1. Take the topic provided by the user
        2. Use the 'search_database' tool to find relevant information
        3. Return only the raw search results, no commentary
        4. If multiple results exist, pick the most relevant one
    """,
    
    # TODO: Assign tools this agent can use (remove if no tools needed)
    tools=toolDB  # This agent uses database tools
    # Alternative: tools=[toolDB, toolFunction] if agent needs both toolsets
)

# --- SECOND AGENT - PROCESSOR/FORMATTER ---
# TODO: Replace this with your second agent's specific job
second_agent = LlmAgent(
    # TODO: Choose your AI model (can be same or different from first agent)
    model='gemini-2.5-flash',
    
    # TODO: Give your agent a descriptive name
    name='formatter_agent',  # Change to match your agent's purpose
    
    # TODO: Write specific instructions for processing the first agent's output
    instruction="""
        REPLACE THIS ENTIRE INSTRUCTION WITH YOUR AGENT'S JOB
        
        Your second agent typically:
        - Takes output from the first agent
        - Processes, analyzes, or transforms it
        - Applies business logic or formatting
        - Creates final user-facing output
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a content formatter. Your job is to:
        1. Take the raw research data from the previous step
        2. Use the 'format_content' tool to create a summary
        3. Make the output engaging and user-friendly
        4. Include key insights and actionable recommendations
    """,
    
    # TODO: Choose which tools this agent needs
    tools=[toolFunction],  # This agent uses live function tools
    # Alternative: tools=toolDB or tools=[toolDB, toolFunction]
)

# TODO: Add more agents if your workflow needs them
# Example third agent:
# final_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='quality_checker',
#     instruction="""
#         You are a quality checker. Review the formatted content and:
#         1. Check for accuracy and completeness
#         2. Ensure proper formatting and tone
#         3. Make final corrections if needed
#         4. Approve or request revisions
#     """,
#     tools=[toolFunction]
# )

# ============================================================================
# ROOT AGENT - ORCHESTRATES THE ENTIRE WORKFLOW
# ============================================================================

# TODO: Configure your main agent system
root_agent = SequentialAgent(
    # TODO: Name your complete system (this becomes your API name)
    name='your_agent_pipeline',  # Change to describe your system's purpose
    
    # TODO: List all agents in the order they should run
    sub_agents=[
        first_agent,   # Runs first
        second_agent   # Runs after first_agent completes
        # Add more agents here if needed
    ],
    
    # TODO: Optional - add description of what your system does
    # description="Processes user input through research and formatting pipeline"
)

# ============================================================================
# ALTERNATIVE CONFIGURATIONS - UNCOMMENT TO USE DIFFERENT PATTERNS
# ============================================================================

# TODO: Use LoopAgent if you want agents to run multiple times
# from google.adk.agents.loop_agent import LoopAgent
# root_agent = LoopAgent(
#     name='your_loop_system',
#     sub_agents=[first_agent, second_agent],
#     max_iterations=3,  # How many times to repeat the sequence
#     description="Runs agents in a loop for iterative processing"
# )

# TODO: Use single LlmAgent if you only need one agent with tools
# root_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='single_agent_system',
#     instruction="Combined instructions for a single agent...",
#     tools=[toolDB, toolFunction]  # Can use multiple toolsets
# )

# ============================================================================
# SERVER DEPLOYMENT - TURNS YOUR AGENTS INTO A WEB API
# ============================================================================

# Import the converter that makes your agents accessible via web API
from agent_to_a2a import to_a2a

# This section runs when you execute this file directly
if __name__ == "__main__":
    import uvicorn  # Fast web server for Python APIs
    
    # TODO: Customize your server settings
    SERVER_PORT = 8080  # Change if you need a different port
    SERVER_HOST = '0.0.0.0'  # '0.0.0.0' accepts connections from anywhere
    
    # Convert your agent system into a web API
    a2a_app = to_a2a(
        root_agent,        # Your main agent system from above
        port=SERVER_PORT,  # Port number for the API
        public_url=PUBLIC_URL  # Public URL from environment variables
    )
    
    # Start the web server (your agents are now live!)
    uvicorn.run(a2a_app, host=SERVER_HOST, port=SERVER_PORT)
    # After this runs, users can send requests to your agent system

# ============================================================================
# ENVIRONMENT VARIABLES SETUP (.env file)
# ============================================================================
"""
Create a file named '.env' in your project folder with these variables:
(Replace the example URLs with your actual service URLs)

# Database tools server (where pre-built tools are stored)
DB_TOOLS_URL=http://your-toolbox-server.com

# Live function tools server (real-time APIs and services)  
FUNCTION_TOOLS_URL=http://your-function-server.com

# Public URL where users can access your agent
PUBLIC_URL=http://your-agent-domain.com

# Add any other environment variables your project needs:
# OPENAI_API_KEY=sk-your-openai-key-here
# DATABASE_PASSWORD=your-db-password-here
# SLACK_BOT_TOKEN=xoxb-your-slack-token
"""

# ============================================================================
# STEP-BY-STEP CUSTOMIZATION GUIDE
# ============================================================================
"""
FOLLOW THESE STEPS TO CUSTOMIZE THIS TEMPLATE:

□ 1. BASIC SETUP
   ✓ Create .env file with your URLs and API keys
   ✓ Install required packages: pip install google-adk toolbox-core uvicorn
   ✓ Test that the script runs without import errors

□ 2. CONFIGURE YOUR TOOLS
   ✓ Set up your toolbox database server (DB_TOOLS_URL)
   ✓ Set up your function tools server (FUNCTION_TOOLS_URL)  
   ✓ Replace 'your-toolset-name' with your actual toolset name
   ✓ Test tool connections work correctly

□ 3. DESIGN YOUR AGENTS
   ✓ Replace first_agent with your data collector/processor
   ✓ Replace second_agent with your formatter/finalizer
   ✓ Write clear, specific instructions for each agent
   ✓ Assign appropriate tools to each agent

□ 4. NAME YOUR SYSTEM
   ✓ Change 'your_agent_pipeline' to a descriptive system name
   ✓ Update agent names to match their purposes
   ✓ Add description if needed for documentation

□ 5. TEST AND DEPLOY
   ✓ Test each agent individually
   ✓ Test the complete pipeline with sample data
   ✓ Configure PORT and HOST for your deployment environment
   ✓ Set PUBLIC_URL for external access

□ 6. OPTIONAL ENHANCEMENTS
   ✓ Add more agents if your workflow is complex
   ✓ Switch to LoopAgent if you need iterative processing
   ✓ Add error handling and validation
   ✓ Implement logging for monitoring
"""

# ============================================================================
# COMPLETE EXAMPLE - BLOG POST CREATION SYSTEM
# ============================================================================
"""
Here's a real example of how to customize this template for a blog post creation system:

# 1. ENVIRONMENT VARIABLES (.env file)
DB_TOOLS_URL=http://content-tools.mycompany.com
FUNCTION_TOOLS_URL=http://writing-tools.mycompany.com  
PUBLIC_URL=http://blog-assistant.mycompany.com

# 2. TOOL SETUP
toolbox = ToolboxSyncClient(DB_TOOLS_URL)
research_tools = toolbox.load_toolset('research-database')  # Tools for finding info
writing_tools = MCPToolset(
    connection_params=SseServerParams(url=FUNCTION_TOOLS_URL, headers={})
)

# 3. FIRST AGENT - Research Assistant
research_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='research_agent',
    instruction=\"\"\"
        You are a research assistant for blog writing. Your job is to:
        1. Take the blog topic provided by the user
        2. Use the 'search_content_database' tool to find relevant information
        3. Use the 'get_trending_topics' tool to find current trends
        4. Return a structured research summary with key points and sources
        5. Focus on finding 3-5 main points that would make good blog sections
    \"\"\",
    tools=research_tools
)

# 4. SECOND AGENT - Blog Writer
writer_agent = LlmAgent(
    model='gemini-2.5-flash', 
    name='blog_writer',
    instruction=\"\"\"
        You are a professional blog writer. Your job is to:
        1. Take the research summary from the previous step
        2. Use the 'generate_outline' tool to create a blog structure
        3. Use the 'write_content' tool to create engaging blog content
        4. Create a complete blog post with intro, body sections, and conclusion
        5. Make it engaging, SEO-friendly, and around 800-1200 words
        6. Include a catchy title and meta description
    \"\"\",
    tools=[writing_tools]
)

# 5. ROOT AGENT - Blog Creation System
root_agent = SequentialAgent(
    name='blog_creation_system',
    sub_agents=[research_agent, writer_agent]
)

# 6. USAGE EXAMPLE
# User input: "Write a blog post about sustainable gardening"
# research_agent: Finds info about sustainable gardening practices
# writer_agent: Creates complete blog post with title, sections, conclusion

# The user gets: A full blog post ready to publish!
"""

# ============================================================================
# MORE USE CASE EXAMPLES
# ============================================================================
"""
OTHER WAYS TO USE THIS TEMPLATE:

1. CUSTOMER SUPPORT PIPELINE
   - Agent 1: Categorizes customer inquiry using classification tools
   - Agent 2: Searches knowledge base and creates personalized response
   
   research_agent → response_agent → final customer reply

2. DATA ANALYSIS WORKFLOW  
   - Agent 1: Cleans and validates data using data tools
   - Agent 2: Performs analysis and creates visualizations
   
   data_cleaner → data_analyzer → insights report

3. SOCIAL MEDIA CONTENT CREATOR
   - Agent 1: Researches trending topics and audience preferences  
   - Agent 2: Creates engaging posts optimized for each platform
   
   trend_researcher → content_creator → social media posts

4. DOCUMENT PROCESSOR
   - Agent 1: Extracts and categorizes information from documents
   - Agent 2: Summarizes and formats into final report
   
   document_parser → report_generator → formatted report

5. PRODUCT RECOMMENDATION ENGINE
   - Agent 1: Analyzes user preferences and browsing history
   - Agent 2: Matches preferences with product catalog and creates recommendations
   
   preference_analyzer → recommendation_engine → personalized suggestions

CUSTOMIZATION FOR EACH EXAMPLE:
- Change agent names and instructions to match the use case
- Configure tools for the specific data sources and APIs needed
- Adjust the model selection based on task complexity
- Modify the toolset names to match your available tools
"""

# ============================================================================
# TROUBLESHOOTING GUIDE
# ============================================================================
"""
COMMON ISSUES AND SOLUTIONS:

PROBLEM: ImportError - can't import google.adk
SOLUTION: Install Google ADK: pip install google-adk

PROBLEM: Tool connection fails
SOLUTION: Check your .env file URLs, make sure servers are running

PROBLEM: Agent gives generic responses
SOLUTION: Make instructions more specific, add examples in instructions

PROBLEM: Agents can't access tools
SOLUTION: Verify tools are assigned correctly in agent definition

PROBLEM: Server won't start
SOLUTION: Check if port is already in use, try different PORT number

PROBLEM: .env variables not loading
SOLUTION: Make sure .env file is in same folder as your script

PROBLEM: Toolset not found
SOLUTION: Check toolset name matches exactly what's in your database

TESTING TIPS:
- Test each agent individually before combining them
- Use print statements to debug data flow between agents
- Check tool responses are what you expect
- Verify .env variables load correctly with print statements
"""
