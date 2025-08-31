"""
A2A Agent Template - Convert Your ADK Agent to A2A Application

This template helps you convert any ADK (Agent Development Kit) agent into an A2A 
(Agent-to-Agent) Starlette web application that can communicate with other agents.

WHAT THIS TEMPLATE DOES:
- Takes your existing ADK agent and wraps it in a web server
- Creates HTTP endpoints for agent communication
- Handles session management, memory, and authentication
- Generates an agent card that describes your agent's capabilities
- Returns a Starlette app that can be run with uvicorn

HOW TO USE THIS TEMPLATE:
1. Replace the import statements in the CUSTOM IMPORTS section
2. Replace the agent creation logic in the AGENT SETUP section
3. Optionally modify service configurations
4. Run with: uvicorn your_module:app --host localhost --port 8000
"""

from __future__ import annotations
import logging
import sys

# CORE A2A IMPORTS - DO NOT MODIFY THESE
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from starlette.applications import Starlette

# CORE ADK IMPORTS - DO NOT MODIFY THESE
from google.adk.agents.base_agent import BaseAgent
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService
from google.adk.cli.utils.logs import setup_adk_logger
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.a2a.executor.a2a_agent_executor import A2aAgentExecutor
from google.adk.a2a.utils.agent_card_builder import AgentCardBuilder

# ============================================================================
# SECTION 1: CUSTOM IMPORTS
# ============================================================================
# REPLACE THIS SECTION WITH YOUR AGENT-SPECIFIC IMPORTS
# 
# Examples of what to add here:
# - Your custom agent class import
# - Any tools or plugins your agent uses
# - Configuration files or environment variables
# - Database connections or external API clients
#
# Example imports:
# from my_project.agents.chat_agent import ChatAgent
# from my_project.tools.calculator import CalculatorTool
# from my_project.config import load_config
# import os

#REPLACE-IMPORT
# TODO: Add your custom imports here
pass  # Remove this line when you add your imports

# ============================================================================
# SECTION 2: CONFIGURATION (OPTIONAL)
# ============================================================================
# Add any configuration loading or environment setup here
#
# Examples:
# CONFIG = load_config()
# API_KEY = os.getenv("MY_API_KEY")
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")


def to_a2a(
    agent: BaseAgent, 
    *, 
    host: str = "0.0.0.0",      # Host address for the server (0.0.0.0 = all interfaces)
    port: int = 8080,           # Port number for the server
    public_url: str | None = None  # Public URL if behind a proxy/load balancer
) -> Starlette:
    """
    Convert an ADK agent to an A2A Starlette application.
    
    PARAMETERS EXPLANATION:
    - agent: Your custom agent instance that inherits from BaseAgent
    - host: Server host address ("0.0.0.0" for all interfaces, "localhost" for local only)
    - port: Port number where your agent will listen for requests
    - public_url: Optional public URL if your agent is behind a proxy or load balancer
    
    RETURNS:
    A Starlette web application that can be run with uvicorn
    
    USAGE EXAMPLE:
    my_agent = MyCustomAgent()
    app = to_a2a(my_agent, host="localhost", port=8000)
    # Then run: uvicorn my_module:app --host localhost --port 8000
    """
    
    # Set up logging so you can see what's happening
    # You can change logging.INFO to logging.DEBUG for more detailed logs
    setup_adk_logger(logging.INFO)

    async def create_runner() -> Runner:
        """
        Create a Runner that manages your agent's lifecycle and services.
        
        The Runner is the core component that:
        - Manages your agent's execution
        - Handles memory, sessions, and artifacts
        - Provides authentication services
        - Manages plugins and tools
        """
        return Runner(
            # Agent name (used for logging and identification)
            app_name=agent.name or "adk_agent",
            
            # Your agent instance
            agent=agent,
            
            # ================================================================
            # SERVICE CONFIGURATION
            # ================================================================
            # These services handle different aspects of agent functionality
            # You can replace these with custom implementations if needed
            
            # Artifact service: handles file storage and management
            artifact_service=InMemoryArtifactService(),
            
            # Session service: manages conversation sessions
            session_service=InMemorySessionService(),
            
            # Memory service: handles agent memory and context
            memory_service=InMemoryMemoryService(),
            
            # Credential service: manages API keys and authentication
            credential_service=InMemoryCredentialService(),
            
            # ================================================================
            # PLUGINS SECTION
            # ================================================================
            # Add your agent's plugins/tools here
            # 
            # Examples:
            # plugins=[
            #     CalculatorTool(),
            #     WebSearchTool(api_key=SEARCH_API_KEY),
            #     DatabaseTool(connection_string=DATABASE_URL),
            # ]
            #
            #REPLACE-PLUGIN
            # TODO: Add your plugins here as a list
            # plugins=[YourTool1(), YourTool2()]
        )

    # ========================================================================
    # A2A INFRASTRUCTURE SETUP
    # ========================================================================
    # This section sets up the A2A communication infrastructure
    # You typically don't need to modify this unless you have special requirements

    # Task store: manages asynchronous task execution
    task_store = InMemoryTaskStore()

    # Agent executor: handles the execution of agent requests
    agent_executor = A2aAgentExecutor(
        runner=create_runner,
    )

    # Request handler: processes incoming HTTP requests
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor, 
        task_store=task_store
    )

    # ========================================================================
    # AGENT CARD GENERATION
    # ========================================================================
    # The agent card describes your agent's capabilities to other agents
    
    # Build URL for agent communication (uses public_url if provided)
    # rpc_url = f"http://{host}:{port}/"  # Uncomment if you want to use host:port instead
    
    card_builder = AgentCardBuilder(
        agent=agent,                    # Your agent instance
        rpc_url=public_url,            # URL where other agents can reach this one
    )

    # ========================================================================
    # STARLETTE APPLICATION SETUP
    # ========================================================================
    # Create the main web application
    
    app = Starlette()

    async def setup_a2a():
        """
        Startup handler that:
        1. Builds the agent card (describes agent capabilities)
        2. Sets up A2A communication routes
        3. Configures the web application
        """
        # Build the agent card asynchronously
        # This card tells other agents what your agent can do
        agent_card = await card_builder.build()

        # Create the A2A application with all necessary components
        a2a_app = A2AStarletteApplication(
            agent_card=agent_card,           # Agent capability description
            http_handler=request_handler,    # Handles incoming requests
        )

        # Add A2A communication routes to the main application
        # This creates endpoints like /health, /execute, /status etc.
        a2a_app.add_routes_to_app(app)

    # Register the setup function to run when the server starts
    app.add_event_handler("startup", setup_a2a)

    return app


# ============================================================================
# SECTION 3: AGENT CREATION AND APP INITIALIZATION
# ============================================================================
# This is where you create your agent instance and convert it to A2A

def create_my_agent() -> BaseAgent:
    """
    Create and configure your custom agent.
    
    REPLACE THIS FUNCTION with your agent creation logic.
    
    Your agent should:
    1. Inherit from BaseAgent
    2. Implement required methods like __call__ or process_message
    3. Have any tools/plugins configured
    4. Be properly initialized with necessary parameters
    
    Example:
    def create_my_agent() -> BaseAgent:
        return ChatAgent(
            name="My Chat Agent",
            description="A helpful chat assistant",
            model="gpt-4",
            tools=[CalculatorTool(), WebSearchTool()]
        )
    """
    #REPLACE-AGENT-CREATION
    # TODO: Replace this with your actual agent creation code
    # This is just a placeholder - you need to implement your actual agent
    raise NotImplementedError(
        "You need to implement create_my_agent() function with your actual agent creation logic"
    )


# ============================================================================
# SECTION 4: APPLICATION ENTRY POINT
# ============================================================================
# This creates the final application that uvicorn will run

# Create your agent instance
# MODIFY THIS LINE to use your agent creation function
my_agent = create_my_agent()

# Convert your agent to an A2A application
# MODIFY THESE PARAMETERS as needed for your deployment
app = to_a2a(
    agent=my_agent,
    host="0.0.0.0",           # Change to "localhost" for local-only access
    port=8080,                # Change port if needed
    public_url=None           # Set if using reverse proxy: "https://my-agent.example.com"
)

# ============================================================================
# HOW TO RUN THIS APPLICATION:
# ============================================================================
# 1. Save this file as 'my_agent_server.py' (or any name you prefer)
# 2. Install dependencies: pip install uvicorn starlette a2a google-adk
# 3. Run with: uvicorn my_agent_server:app --host 0.0.0.0 --port 8080
# 4. Your agent will be available at http://localhost:8080

# ============================================================================
# EXAMPLE IMPLEMENTATION
# ============================================================================
"""
Here's a complete example of how to fill out this template for a simple chat agent:

# SECTION 1: CUSTOM IMPORTS (replace #REPLACE-IMPORT)
from my_project.agents.simple_chat_agent import SimpleChatAgent
from my_project.tools.weather_tool import WeatherTool
from my_project.tools.calculator_tool import CalculatorTool
import os

# SECTION 2: CONFIGURATION
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
AGENT_NAME = "Weather Chat Assistant"

# SECTION 3: AGENT CREATION (replace create_my_agent function)
def create_my_agent() -> BaseAgent:
    return SimpleChatAgent(
        name=AGENT_NAME,
        description="A helpful assistant that can check weather and do calculations",
        system_prompt="You are a helpful assistant specialized in weather and math.",
        tools=[
            WeatherTool(api_key=WEATHER_API_KEY),
            CalculatorTool()
        ]
    )

# SECTION 4: REPLACE AGENT CREATION (replace #REPLACE-AGENT-CREATION)
# Just make sure create_my_agent() returns your actual agent

# SECTION 5: PLUGINS (if your Runner needs plugins, replace #REPLACE-PLUGIN)
# In the create_runner function, add:
# plugins=[
#     WeatherTool(api_key=WEATHER_API_KEY),
#     CalculatorTool()
# ]

RUNNING THE EXAMPLE:
1. pip install uvicorn starlette a2a google-adk my_project
2. uvicorn my_agent_server:app --host localhost --port 8080
3. Agent available at http://localhost:8080
4. Other agents can communicate with it via the A2A protocol
"""
