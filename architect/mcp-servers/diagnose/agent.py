# =====================================
# MCP AGENT TEMPLATE - Complete Guide
# =====================================
# This template helps you create a multi-agent system that can:
# 1. Connect to multiple MCP tool servers
# 2. Use database tools via toolbox
# 3. Coordinate between specialized agents
# 4. Handle complex workflows with delegation

import asyncio
import os
from contextlib import AsyncExitStack
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
import logging 
import nest_asyncio 
from toolbox_core import ToolboxSyncClient

# =====================================
# ENVIRONMENT SETUP SECTION
# =====================================
# Load environment variables - ALWAYS keep this at the top
load_dotenv()

# Configure logging - CUSTOMIZE: Change log level if needed (DEBUG, INFO, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# =====================================
# GLOBAL VARIABLES SECTION
# =====================================
# DO NOT MODIFY: These are needed for proper agent lifecycle management
root_agent: LlmAgent | None = None
exit_stack: AsyncExitStack | None = None

# =====================================
# URL CONFIGURATION SECTION
# =====================================
# REPLACE THESE: Set your MCP server URLs in environment variables
# These should point to your running MCP servers

# CUSTOMIZE: Database tools URL (from your db-toolbox server)
DB_TOOLS_URL = os.environ.get("DB_TOOLS_URL")
# Example: "http://localhost:8080" or "https://your-db-server.com"

# CUSTOMIZE: API tools URL (from your function-based MCP server)
API_TOOLS_URL = os.environ.get("API_TOOLS_URL") 
# Example: "http://localhost:8081" or "https://your-api-server.com"

# CUSTOMIZE: Function tools URL (from another MCP server if you have one)
FUNCTION_TOOLS_URL = os.environ.get("FUNCTION_TOOLS_URL")
# Example: "http://localhost:8082" or "https://your-function-server.com"

# ADD MORE URLS: If you have additional MCP servers
# EXTRA_TOOLS_URL = os.environ.get("EXTRA_TOOLS_URL")

# Debug print statements - CUSTOMIZE: Update these to match your URLs
print(f"DB_TOOLS_URL: {DB_TOOLS_URL}")
print(f"API_TOOLS_URL: {API_TOOLS_URL}")
print(f"FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")

# =====================================
# AGENT CREATION FUNCTION
# =====================================
async def get_agent_async():
    """
    Creates and configures your multi-agent system.
    
    CUSTOMIZE THIS FUNCTION: Modify to create your own agents and tool connections.
    
    Returns:
        LlmAgent: The main coordinating agent
    """
    
    # Print URLs for debugging
    print(f"Connecting to DB_TOOLS_URL: {DB_TOOLS_URL}")
    print(f"Connecting to API_TOOLS_URL: {API_TOOLS_URL}")
    print(f"Connecting to FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")

    # =====================================
    # TOOLSET CONNECTIONS SECTION
    # =====================================
    # CUSTOMIZE: Connect to your database toolbox
    toolbox = ToolboxSyncClient(DB_TOOLS_URL)
    
    # REPLACE: Load your specific toolset from the database server
    # This should match a toolset name from your tools.yaml file
    toolDB = toolbox.load_toolset('YOUR-TOOLSET-NAME')  # Replace with your actual toolset name
    
    # CUSTOMIZE: Connect to your API-based MCP servers
    toolAPI = MCPToolset(
        connection_params=SseServerParams(url=API_TOOLS_URL, headers={})
    )
    
    toolFunction = MCPToolset(
        connection_params=SseServerParams(url=FUNCTION_TOOLS_URL, headers={})
    )
    
    # ADD MORE TOOLSETS: Connect to additional MCP servers if needed
    # toolExtra = MCPToolset(
    #     connection_params=SseServerParams(url=EXTRA_TOOLS_URL, headers={})
    # )

    # =====================================
    # SPECIALIZED AGENTS SECTION
    # =====================================
    # REPLACE THESE: Create your own specialized agents
    
    # AGENT 1: Database/Information Retrieval Agent
    # CUSTOMIZE: This agent handles data lookup and retrieval
    db_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Choose your preferred model
        name='YOUR_DB_AGENT_NAME',  # REPLACE: Give your agent a meaningful name
        instruction="""
            REPLACE THIS INSTRUCTION: Define what this agent does.
            
            Example instructions:
            - "You are a Data Analyst. Your job is to query databases and retrieve information."
            - "You are a Customer Service Agent. Look up customer data and order history."
            - "You are a Research Assistant. Search databases for relevant information."
            
            Be specific about:
            - What this agent should do
            - What tools it should use
            - What it should NOT do
        """,
        tools=toolDB  # This agent uses database tools
    )
    
    # AGENT 2: Action/API Agent  
    # CUSTOMIZE: This agent handles actions and external API calls
    api_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Choose your preferred model
        name='YOUR_API_AGENT_NAME',  # REPLACE: Give your agent a meaningful name
        instruction="""
            REPLACE THIS INSTRUCTION: Define what this agent does.
            
            Example instructions:
            - "You are an Integration Agent. Execute API calls and external actions."
            - "You are a Notification Agent. Send emails, SMS, and push notifications."
            - "You are an Automation Agent. Trigger workflows and process data."
            
            Be specific about:
            - What actions this agent can perform
            - Which APIs it should call
            - Any limitations or safety guidelines
        """,
        tools=[toolFunction, toolAPI]  # This agent uses function and API tools
    )
    
    # ADD MORE AGENTS: Create additional specialized agents if needed
    # analytics_agent = LlmAgent(
    #     model='gemini-2.5-flash',
    #     name='analytics_agent',
    #     instruction="You analyze data and generate reports.",
    #     tools=toolExtra
    # )

    # =====================================
    # MASTER COORDINATOR AGENT
    # =====================================
    # CUSTOMIZE: This is your main agent that delegates to specialists
    root_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Choose your preferred model
        name='YOUR_MASTER_AGENT_NAME',  # REPLACE: Name your coordinator agent
        instruction="""
            REPLACE THIS INSTRUCTION: Define how your master agent delegates tasks.
            
            You are the Master Coordinator. Your job is to analyze user requests 
            and delegate them to the right specialist agent.
            
            CUSTOMIZE: List your agents and their roles:
            - **YOUR_DB_AGENT_NAME**: Handles all data lookup, search, and retrieval tasks
            - **YOUR_API_AGENT_NAME**: Handles all actions, API calls, and external operations
            
            DELEGATION RULES:
            - For questions about existing data → delegate to YOUR_DB_AGENT_NAME
            - For actions that change things → delegate to YOUR_API_AGENT_NAME
            - For analysis tasks → delegate to [specify which agent]
            
            You do NOT perform tasks yourself - you only coordinate and delegate.
        """,
        sub_agents=[db_agent, api_agent],  # LIST: Include all your specialized agents
        # sub_agents=[db_agent, api_agent, analytics_agent],  # ADD MORE: Include additional agents
    )
    
    print("✅ Multi-agent system created successfully.")
    return root_agent

# =====================================
# INITIALIZATION FUNCTION
# =====================================
# DO NOT MODIFY: This function handles proper agent initialization
async def initialize():
    """Initializes the global root_agent safely."""
    global root_agent
    if root_agent is None:
        log.info("🔄 Initializing agent system...")
        root_agent = await get_agent_async()
        if root_agent:
            log.info("✅ Agent system initialized successfully.")
        else:
            log.error("❌ Agent system initialization failed.")
    else:
        log.info("ℹ️  Agent system already initialized.")

# =====================================
# MODULE STARTUP SECTION
# =====================================
# DO NOT MODIFY: This handles the async initialization properly
nest_asyncio.apply()

log.info("🚀 Starting agent initialization...")
try:
    asyncio.run(initialize())
    log.info("✅ Module initialization completed successfully.")
except RuntimeError as e:
    log.error(f"⚠️  RuntimeError during initialization (likely nested loops): {e}", exc_info=True)
except Exception as e:
    log.error(f"❌ Unexpected error during initialization: {e}", exc_info=True)

# =====================================
# OPTIONAL: ADDITIONAL FUNCTIONS
# =====================================
# ADD YOUR OWN: Create helper functions for your specific use case

def get_agent():
    """
    OPTIONAL: Synchronous wrapper to get the initialized agent.
    CUSTOMIZE: Add your own helper functions here.
    """
    global root_agent
    if root_agent is None:
        raise RuntimeError("Agent not initialized. Call initialize() first.")
    return root_agent

# ADD MORE HELPERS: Create additional utility functions as needed
# def reset_agent():
#     """Resets the agent system."""
#     global root_agent
#     root_agent = None

# def is_agent_ready():
#     """Checks if the agent system is ready."""
#     return root_agent is not None

# =====================================
# ENVIRONMENT VARIABLES GUIDE
# =====================================
"""
CREATE A .env FILE with these variables:

# Database Tools Server
DB_TOOLS_URL=http://localhost:8080

# API Tools Server  
API_TOOLS_URL=http://localhost:8081

# Function Tools Server
FUNCTION_TOOLS_URL=http://localhost:8082

# Add any additional MCP server URLs:
# EXTRA_TOOLS_URL=http://localhost:8083

# Add any API keys or secrets:
# OPENAI_API_KEY=your_openai_key
# DATABASE_PASSWORD=your_db_password
"""

# =====================================
# COMPLETE EXAMPLE: CUSTOMER SERVICE SYSTEM
# =====================================
"""
EXAMPLE CONFIGURATION: Customer Service Multi-Agent System
---------------------------------------------------------

Environment Variables (.env file):
DB_TOOLS_URL=http://localhost:8080
API_TOOLS_URL=http://localhost:8081  
NOTIFICATION_TOOLS_URL=http://localhost:8082

Agent Configuration:

# Database Agent - Handles customer data lookup
customer_data_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='customer_data_agent',
    instruction='''
        You are a Customer Data Specialist. Your role is to:
        - Look up customer information and order history
        - Search product catalogs and inventory
        - Retrieve account details and preferences
        - Find transaction records and billing information
        
        Use your database tools to answer questions about existing data.
        You do NOT create, update, or delete anything.
    ''',
    tools=customer_db_tools
)

# Action Agent - Handles operations and notifications
customer_action_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='customer_action_agent', 
    instruction='''
        You are a Customer Action Specialist. Your role is to:
        - Send notifications (email, SMS, push)
        - Process refunds and cancellations
        - Update customer preferences
        - Create support tickets
        - Trigger automated workflows
        
        Use your API tools to perform actions and make changes.
        Always confirm actions before executing them.
    ''',
    tools=[notification_tools, api_tools]
)

# Master Coordinator
customer_service_coordinator = LlmAgent(
    model='gemini-2.5-flash',
    name='customer_service_coordinator',
    instruction='''
        You are the Customer Service Coordinator. Analyze requests and delegate:
        
        DELEGATE TO customer_data_agent:
        - "What's my order status?"
        - "Show me my purchase history"
        - "Do you have this product in stock?"
        - "What's my account balance?"
        
        DELEGATE TO customer_action_agent:
        - "Cancel my order"
        - "Send me a receipt"
        - "Update my email address"
        - "Process my refund"
        
        You coordinate but don't perform the actual work.
    ''',
    sub_agents=[customer_data_agent, customer_action_agent]
)

EXAMPLE 2: Content Management System
----------------------------------

# Content Retrieval Agent
content_retrieval_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='content_retrieval_agent',
    instruction='''
        You are a Content Librarian. You:
        - Search articles, blogs, and documents
        - Retrieve user-generated content
        - Find media files and metadata
        - Look up content analytics and stats
        
        Use database tools to find existing content.
    ''',
    tools=content_db_tools
)

# Content Management Agent  
content_management_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='content_management_agent',
    instruction='''
        You are a Content Manager. You:
        - Publish new articles and posts
        - Update existing content
        - Moderate and approve submissions
        - Send content notifications
        - Manage content workflows
        
        Use API tools to create and modify content.
    ''',
    tools=[publishing_tools, moderation_tools]
)

# Content Coordinator
content_coordinator = LlmAgent(
    model='gemini-2.5-flash',
    name='content_coordinator',
    instruction='''
        You coordinate content operations:
        
        For SEARCHING/FINDING content → delegate to content_retrieval_agent
        For CREATING/UPDATING content → delegate to content_management_agent
    ''',
    sub_agents=[content_retrieval_agent, content_management_agent]
)

EXAMPLE 3: E-commerce Analytics System
------------------------------------

# Data Analysis Agent
analytics_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='analytics_agent',
    instruction='''
        You are a Business Intelligence Analyst. You:
        - Generate sales reports and metrics
        - Analyze customer behavior patterns
        - Track inventory trends
        - Calculate KPIs and performance metrics
        
        Use database tools to query and analyze data.
    ''',
    tools=analytics_db_tools
)

# Automation Agent
automation_agent = LlmAgent(
    model='gemini-2.5-flash', 
    name='automation_agent',
    instruction='''
        You are an Operations Automation Specialist. You:
        - Trigger marketing campaigns
        - Send automated reports
        - Update inventory levels
        - Process bulk operations
        
        Use API tools to execute automated tasks.
    ''',
    tools=[marketing_tools, inventory_tools]
)

# Business Coordinator
business_coordinator = LlmAgent(
    model='gemini-2.5-flash',
    name='business_coordinator', 
    instruction='''
        You coordinate business operations:
        
        For REPORTS/ANALYSIS → delegate to analytics_agent
        For AUTOMATION/ACTIONS → delegate to automation_agent
    ''',
    sub_agents=[analytics_agent, automation_agent]
)
"""

# =====================================
# AGENT CREATION FUNCTION
# =====================================
async def get_agent_async():
    """
    Creates and configures your multi-agent system.
    
    MAIN CUSTOMIZATION AREA: This is where you define your agents and their roles.
    
    Returns:
        LlmAgent: The main coordinating agent
    """
    
    # Debug print statements
    print(f"🔗 Connecting to DB_TOOLS_URL: {DB_TOOLS_URL}")
    print(f"🔗 Connecting to API_TOOLS_URL: {API_TOOLS_URL}")
    print(f"🔗 Connecting to FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")

    # =====================================
    # TOOLSET CONNECTIONS
    # =====================================
    # STEP 1: Connect to your database toolbox server
    toolbox = ToolboxSyncClient(DB_TOOLS_URL)
    
    # REPLACE: Load your specific toolset (must match name in tools.yaml)
    toolDB = toolbox.load_toolset('YOUR-TOOLSET-NAME')  
    # Example: toolDB = toolbox.load_toolset('customer-management')
    
    # STEP 2: Connect to your MCP function servers
    # CUSTOMIZE: Add connection parameters and headers if needed
    toolAPI = MCPToolset(
        connection_params=SseServerParams(url=API_TOOLS_URL, headers={})
    )
    
    toolFunction = MCPToolset(
        connection_params=SseServerParams(url=FUNCTION_TOOLS_URL, headers={})
    )
    
    # ADD MORE: Connect to additional MCP servers
    # toolExtra = MCPToolset(
    #     connection_params=SseServerParams(url=EXTRA_TOOLS_URL, headers={})
    # )

    # =====================================
    # SPECIALIZED AGENTS CREATION
    # =====================================
    # AGENT 1: Database/Retrieval Specialist
    # CUSTOMIZE: This agent handles all data retrieval operations
    db_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Change model if needed (gpt-4, claude-3, etc.)
        name='YOUR_DB_AGENT_NAME',  # REPLACE: Choose a descriptive name
        instruction="""
            REPLACE THIS ENTIRE INSTRUCTION with your agent's role.
            
            TEMPLATE:
            You are a [ROLE NAME]. Your job is to:
            - [What this agent does - be specific]
            - [What tools it uses]
            - [What it should NOT do]
            
            EXAMPLES:
            - Data lookup and search operations
            - Customer information retrieval  
            - Product catalog queries
            - Historical data analysis
            
            Use your database tools to find and retrieve information.
            You do NOT create, update, or delete data.
        """,
        tools=toolDB  # Uses database tools only
    )
    
    # AGENT 2: Action/API Specialist
    # CUSTOMIZE: This agent handles all action-based operations
    api_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Change model if needed
        name='YOUR_API_AGENT_NAME',  # REPLACE: Choose a descriptive name
        instruction="""
            REPLACE THIS ENTIRE INSTRUCTION with your agent's role.
            
            TEMPLATE:
            You are a [ROLE NAME]. Your job is to:
            - [What actions this agent performs]
            - [What APIs it calls]
            - [What changes it can make]
            
            EXAMPLES:
            - Send notifications and communications
            - Process payments and transactions
            - Update records and preferences
            - Trigger automated workflows
            
            Use your API and function tools to perform actions and make changes.
            Always confirm important actions before executing.
        """,
        tools=[toolFunction, toolAPI]  # Uses function and API tools
    )
    
    # ADD MORE AGENTS: Create additional specialists if needed
    # analysis_agent = LlmAgent(
    #     model='gemini-2.5-flash',
    #     name='analysis_agent',
    #     instruction="You perform data analysis and generate insights.",
    #     tools=toolExtra
    # )

    # =====================================
    # MASTER COORDINATOR AGENT
    # =====================================
    # CUSTOMIZE: This is your main orchestrating agent
    root_agent = LlmAgent(
        model='gemini-2.5-flash',  # CUSTOMIZE: Change model if needed
        name='YOUR_MASTER_COORDINATOR_NAME',  # REPLACE: Name your main agent
        instruction="""
            REPLACE THIS ENTIRE INSTRUCTION with your coordination logic.
            
            TEMPLATE:
            You are the [SYSTEM NAME] Coordinator. Your role is to analyze user requests 
            and delegate them to the correct specialist agent.
            
            You command these specialists:
            - **YOUR_DB_AGENT_NAME**: Delegate requests for [describe when to use]
            - **YOUR_API_AGENT_NAME**: Delegate requests for [describe when to use]
            
            DELEGATION EXAMPLES:
            - Questions starting with "What", "Show me", "Find" → YOUR_DB_AGENT_NAME
            - Actions starting with "Send", "Create", "Update", "Process" → YOUR_API_AGENT_NAME
            
            IMPORTANT: You analyze and delegate only. You do NOT perform tasks yourself.
        """,
        sub_agents=[db_agent, api_agent],  # LIST: All your specialized agents
        # sub_agents=[db_agent, api_agent, analysis_agent],  # ADD MORE: Include additional agents
    )
    
    print("✅ Multi-agent system created successfully.")
    return root_agent

# =====================================
# INITIALIZATION HANDLER
# =====================================
# DO NOT MODIFY: This section handles proper async initialization
async def initialize():
    """Initializes the global root_agent safely."""
    global root_agent
    if root_agent is None:
        log.info("🔄 Initializing agent system...")
        root_agent = await get_agent_async()
        if root_agent:
            log.info("✅ Agent system initialized successfully.")
        else:
            log.error("❌ Agent system initialization failed.")
    else:
        log.info("ℹ️  Agent system already initialized.")

# =====================================
# MODULE STARTUP EXECUTION
# =====================================
# DO NOT MODIFY: This starts the initialization process
nest_asyncio.apply()

log.info("🚀 Starting agent system initialization...")
try:
    asyncio.run(initialize())
    log.info("✅ Module initialization completed successfully.")
except RuntimeError as e:
    log.error(f"⚠️  RuntimeError during initialization: {e}", exc_info=True)
except Exception as e:
    log.error(f"❌ Unexpected error during initialization: {e}", exc_info=True)

# =====================================
# OPTIONAL: UTILITY FUNCTIONS
# =====================================
# ADD YOUR OWN: Create helper functions for your application

def get_agent():
    """
    Synchronous wrapper to get the initialized agent.
    CUSTOMIZE: Add error handling specific to your use case.
    """
    global root_agent
    if root_agent is None:
        raise RuntimeError("❌ Agent system not initialized. Call initialize() first.")
    return root_agent

def is_system_ready():
    """
    Checks if the agent system is fully initialized and ready.
    CUSTOMIZE: Add additional readiness checks if needed.
    """
    return root_agent is not None

# ADD MORE UTILITIES: Create functions specific to your application
# def restart_system():
#     """Restarts the entire agent system."""
#     global root_agent
#     root_agent = None
#     asyncio.run(initialize())

# def get_system_status():
#     """Returns detailed status of the agent system."""
#     return {
#         "initialized": root_agent is not None,
#         "agents_count": len(root_agent.sub_agents) if root_agent else 0,
#         "db_connected": DB_TOOLS_URL is not None,
#         "api_connected": API_TOOLS_URL is not None
#     }

# =====================================
# TEMPLATE CUSTOMIZATION CHECKLIST
# =====================================
"""
STEP-BY-STEP CUSTOMIZATION GUIDE:
=================================

1. ENVIRONMENT SETUP:
   □ Create .env file with your MCP server URLs
   □ Add any API keys or database credentials
   □ Set up your MCP servers (db-toolbox, function servers)

2. TOOLSET CONFIGURATION:
   □ Replace 'YOUR-TOOLSET-NAME' with your actual toolset from tools.yaml
   □ Update DB_TOOLS_URL, API_TOOLS_URL, FUNCTION_TOOLS_URL
   □ Add additional toolset connections if needed

3. AGENT CUSTOMIZATION:
   □ Replace 'YOUR_DB_AGENT_NAME' with a meaningful name
   □ Replace 'YOUR_API_AGENT_NAME' with a meaningful name  
   □ Replace 'YOUR_MASTER_COORDINATOR_NAME' with a meaningful name
   □ Update all agent instructions with your specific roles
   □ Add additional specialized agents if needed

4. DELEGATION LOGIC:
   □ Define clear rules for when to use each agent
   □ Update the master coordinator's delegation instructions
   □ Test that requests are routed to the correct agents

5. TESTING:
   □ Verify all MCP servers are running
   □ Test database connections
   □ Verify agent initialization
   □ Test end-to-end workflows

COMMON USE CASES:
================
- Customer Service (data lookup + actions)
- Content Management (search + publishing)
- E-commerce Operations (catalog + orders)
- Business Intelligence (analysis + reporting)
- IT Operations (monitoring + automation)
- Financial Services (data + transactions)
"""
