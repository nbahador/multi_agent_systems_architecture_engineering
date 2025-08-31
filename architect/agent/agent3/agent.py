# ============================================================================
# REMOTE AGENT ORCHESTRATOR TEMPLATE - Managing Multiple Agent Services
# ============================================================================
# This template creates a master agent that coordinates multiple remote agent services
# Perfect for: Microservices architecture, distributed agent systems, service orchestration
# Uses RemoteA2aAgent to connect to agents running on different servers
# ============================================================================

# --- IMPORTS SECTION ---
# These libraries handle remote agent connections and orchestration

from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH  # Standard path for agent info
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent  # Connects to remote agent services
from google.adk.agents.sequential_agent import SequentialAgent  # Runs agents one after another
from google.adk.agents.llm_agent import LlmAgent  # Creates master orchestrator agent
import os  # Reads environment variables
from google.adk.tools import load_memory  # Loads agent memory/state
from google.adk.tools.tool_context import ToolContext  # Context for tool callbacks
from typing import Dict, Any, Optional  # Type hints for better code

# ============================================================================
# ENVIRONMENT CONFIGURATION - REMOTE AGENT SERVICE URLS
# ============================================================================

# TODO: Replace these with your actual remote agent service URLs
# Each URL should point to a running agent service on different servers/ports

# TODO: Set URL for your first remote agent service
FIRST_AGENT_URL = os.environ.get("FIRST_AGENT_URL", "http://first-agent.example.com")

# TODO: Set URL for your second remote agent service  
SECOND_AGENT_URL = os.environ.get("SECOND_AGENT_URL", "http://second-agent.example.com")

# TODO: Set URL for your third remote agent service
THIRD_AGENT_URL = os.environ.get("THIRD_AGENT_URL", "http://third-agent.example.com")

# Print URLs to verify they loaded correctly from environment
print(f"FIRST_AGENT_URL: {FIRST_AGENT_URL}")
print(f"SECOND_AGENT_URL: {SECOND_AGENT_URL}")  
print(f"THIRD_AGENT_URL: {THIRD_AGENT_URL}")

# ============================================================================
# REMOTE AGENT DEFINITIONS - CONNECT TO EXTERNAL AGENT SERVICES
# ============================================================================

# --- FIRST REMOTE AGENT CONNECTION ---
# TODO: Replace with your first remote agent service
first_remote_agent = RemoteA2aAgent(
    # TODO: Give this remote agent a descriptive name
    name="first_service_agent",  # Change to match what this service does
    
    # TODO: Write a brief description of what this remote agent does
    description="Handles initial data processing",  # Describe the service's purpose
    
    # Build the agent card URL (this is where agent info is stored)
    # The agent card tells us what this remote agent can do
    agent_card=(
        f"{FIRST_AGENT_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"  # Standard path for agent metadata
        # AGENT_CARD_WELL_KNOWN_PATH is usually "/.well-known/agent_card"
    ),
)

# --- SECOND REMOTE AGENT CONNECTION ---
# TODO: Replace with your second remote agent service
second_remote_agent = RemoteA2aAgent(
    # TODO: Give this remote agent a descriptive name
    name="second_service_agent",  # Change to match what this service does
    
    # TODO: Write a brief description of what this remote agent does  
    description="Performs analysis and computation",  # Describe the service's purpose
    
    # Build the agent card URL for this service
    agent_card=(
        f"{SECOND_AGENT_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"  # Gets agent info from remote service
    ),
)

# --- THIRD REMOTE AGENT CONNECTION ---
# TODO: Replace with your third remote agent service
third_remote_agent = RemoteA2aAgent(
    # TODO: Give this remote agent a descriptive name
    name="third_service_agent",  # Change to match what this service does
    
    # TODO: Write a brief description of what this remote agent does
    description="Formats and finalizes output",  # Describe the service's purpose
    
    # Build the agent card URL for this service
    agent_card=(
        f"{THIRD_AGENT_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"  # Gets agent info from remote service
    ),
)

# TODO: Add more remote agents if you have additional services
# Example:
# validation_agent = RemoteA2aAgent(
#     name="validation_service",
#     description="Validates and quality-checks results",
#     agent_card=f"{VALIDATION_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"
# )

# ============================================================================
# CALLBACK FUNCTIONS - HANDLE EVENTS DURING AGENT EXECUTION
# ============================================================================

def save_last_action_callback(
    tool,  # The tool/agent that just finished running
    args: Dict[str, Any],  # Arguments that were passed to the tool
    tool_context: ToolContext,  # Context object containing state and metadata
    tool_response: Dict[str, Any],  # Response returned by the tool
) -> Optional[Dict[str, Any]]:
    """
    Callback function that runs AFTER each remote agent finishes.
    This saves information about what just happened for future reference.
    
    HOW TO CUSTOMIZE:
    - Change what gets saved to state
    - Add logging or monitoring
    - Modify the state key names
    - Add additional processing of tool responses
    
    Args:
        tool: The agent/tool that just executed
        args: Arguments passed to the agent
        tool_context: Contains state and other context info
        tool_response: What the agent returned
        
    Returns:
        The original tool_response (unmodified) or modified version
    """
    # Get the name of the agent that just finished
    agent_name = tool.name
    print(f"[Callback] After agent '{agent_name}' executed with args: {args}")

    # TODO: Customize what information you want to save
    # Save the agent name to state so other agents know what happened last
    print(f"[Callback] Saving last executed agent: {agent_name}")
    tool_context.state["last_action"] = agent_name  # Save under 'last_action' key
    
    # TODO: Add more state tracking if needed
    # Examples:
    # tool_context.state["execution_count"] = tool_context.state.get("execution_count", 0) + 1
    # tool_context.state["last_args"] = args
    # tool_context.state["last_response_size"] = len(str(tool_response))
    
    # IMPORTANT: Return the original response so the next agent gets the right data
    return tool_response

# TODO: Add more callback functions if needed
# Example - callback that runs BEFORE each agent:
# def pre_execution_callback(tool_context: ToolContext) -> None:
#     """Runs before each agent starts"""
#     print(f"[Pre-Callback] About to execute agent...")
#     # Add your pre-execution logic here

# ============================================================================
# MASTER ORCHESTRATOR AGENT - COORDINATES ALL REMOTE SERVICES
# ============================================================================

# TODO: Replace this with your master orchestrator logic
root_agent = LlmAgent(
    # TODO: Name your orchestrator system
    name="master_orchestrator",  # Change to describe your system's purpose
    
    # TODO: Choose AI model for the orchestrator
    model="gemini-2.5-flash",  # The AI that decides which remote agents to call
    
    # TODO: Write comprehensive instructions for your orchestrator
    instruction="""
        REPLACE THIS ENTIRE INSTRUCTION WITH YOUR ORCHESTRATOR'S LOGIC
        
        You are the master coordinator who decides which remote services to use.
        
        YOUR RESPONSIBILITIES:
        1. Analyze incoming user requests
        2. Decide which remote agent(s) to call and in what order
        3. Track what services have been used (via state)
        4. Handle service availability and errors
        5. Coordinate data flow between services
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a Master Coordinator for distributed services. Your job is to:
        
        1. **Request Analysis**: Understand what the user needs
        2. **Service Selection**: Choose the best remote agent for the task
        3. **State Tracking**: Check 'last_action' in state to see what was done previously
        4. **Avoid Overuse**: Don't call the same service repeatedly unless necessary
        5. **Error Handling**: If a service fails, try an alternative approach
        
        AVAILABLE SERVICES (your sub_agents):
        - first_service_agent: Handles data collection and initial processing
        - second_service_agent: Performs analysis and computation  
        - third_service_agent: Formats results and creates final output
        
        DECISION LOGIC:
        - For data requests: Use first_service_agent
        - For analysis tasks: Use second_service_agent  
        - For formatting/output: Use third_service_agent
        - Check state['last_action'] to avoid calling same service twice in a row
    """,
    
    # TODO: List all your remote agents that this orchestrator can call
    sub_agents=[
        first_remote_agent,   # Can call this remote service
        second_remote_agent,  # Can call this remote service
        third_remote_agent    # Can call this remote service
        # Add more remote agents here if you have additional services
    ],
    
    # TODO: Add callbacks to track and manage agent execution
    after_tool_callback=save_last_action_callback,  # Runs after each remote agent call
    # Optional: before_tool_callback=pre_execution_callback,  # Runs before each call
)

# ============================================================================
# ALTERNATIVE ORCHESTRATION PATTERNS - CHOOSE WHAT FITS YOUR NEEDS
# ============================================================================

# TODO: Use SequentialAgent if you want to call remote agents in a fixed order
# root_agent = SequentialAgent(
#     name="sequential_service_coordinator",
#     sub_agents=[
#         first_remote_agent,   # Always runs first
#         second_remote_agent,  # Always runs second  
#         third_remote_agent    # Always runs third
#     ],
#     description="Calls remote services in a fixed sequence"
# )

# TODO: Use this pattern if you want a simple proxy to one remote service
# root_agent = RemoteA2aAgent(
#     name="simple_proxy",
#     description="Direct proxy to single remote service", 
#     agent_card=f"{FIRST_AGENT_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"
# )

# ============================================================================
# SERVER DEPLOYMENT - EXPOSE YOUR ORCHESTRATOR AS A WEB API
# ============================================================================

# Import the converter that makes agents into web APIs
from agent_to_a2a import to_a2a

# TODO: Set your public URL for this orchestrator service
PUBLIC_URL = os.environ.get("PUBLIC_URL", "http://0.0.0.0:8080")  # Default fallback URL

# This runs when you execute this file directly (not when importing)
if __name__ == "__main__":
    import uvicorn  # Fast Python web server
    
    # TODO: Customize your server deployment settings
    SERVER_PORT = 8080  # Change if you need different port
    SERVER_HOST = '0.0.0.0'  # '0.0.0.0' allows external connections
    
    # Convert your orchestrator agent into a web API
    a2a_app = to_a2a(
        root_agent,        # Your orchestrator agent from above
        port=SERVER_PORT,  # Port for this orchestrator service
        public_url=PUBLIC_URL  # Public URL from environment
    )
    
    # Start the orchestrator web server
    uvicorn.run(a2a_app, host=SERVER_HOST, port=SERVER_PORT)
    # Now your orchestrator is live and can coordinate remote services!

# ============================================================================
# ENVIRONMENT VARIABLES SETUP (.env file)
# ============================================================================
"""
Create a '.env' file in your project folder with these variables:
(Replace example URLs with your actual remote service URLs)

# URLs for your remote agent services
FIRST_AGENT_URL=http://data-processor.mycompany.com
SECOND_AGENT_URL=http://analyzer.mycompany.com  
THIRD_AGENT_URL=http://formatter.mycompany.com

# Public URL for this orchestrator service
PUBLIC_URL=http://orchestrator.mycompany.com

# Add any authentication or configuration needed for remote services:
# REMOTE_API_KEY=your-api-key-for-remote-services
# AUTH_TOKEN=bearer-token-for-secure-services
"""

# ============================================================================
# STEP-BY-STEP CUSTOMIZATION GUIDE
# ============================================================================
"""
TO CUSTOMIZE THIS TEMPLATE FOR YOUR DISTRIBUTED SYSTEM:

□ 1. PLAN YOUR ARCHITECTURE
   ✓ Identify what remote services you need to coordinate
   ✓ Determine if you need sequential or intelligent orchestration
   ✓ Plan how data flows between services
   ✓ Design your service URLs and naming convention

□ 2. SET UP REMOTE SERVICES
   ✓ Deploy your individual agent services on different servers/ports
   ✓ Ensure each service exposes the agent card at /.well-known/agent_card
   ✓ Test that each service is accessible and responding
   ✓ Record the URLs for each service

□ 3. CONFIGURE ENVIRONMENT
   ✓ Create .env file with all your remote service URLs
   ✓ Set PUBLIC_URL for where this orchestrator will be deployed
   ✓ Add any authentication tokens or API keys needed
   ✓ Test that environment variables load correctly

□ 4. CUSTOMIZE REMOTE AGENTS
   ✓ Replace first_remote_agent with connection to your first service
   ✓ Replace second_remote_agent with connection to your second service
   ✓ Add more remote agents for additional services
   ✓ Update names and descriptions to match your services

□ 5. DESIGN ORCHESTRATOR LOGIC
   ✓ Write detailed instructions for how to coordinate services
   ✓ Define decision logic for which service to call when
   ✓ Implement state tracking to avoid redundant calls
   ✓ Add error handling for service failures

□ 6. CONFIGURE CALLBACKS
   ✓ Customize save_last_action_callback to track what you need
   ✓ Add additional callbacks for monitoring or logging
   ✓ Implement any business logic that should run between service calls

□ 7. DEPLOY AND TEST
   ✓ Deploy orchestrator service on your chosen server
   ✓ Test connections to all remote services
   ✓ Test complete workflows end-to-end
   ✓ Monitor performance and error rates
"""

# ============================================================================
# COMPLETE EXAMPLE - E-COMMERCE ORDER PROCESSING SYSTEM
# ============================================================================
"""
Here's a real example: An e-commerce system that coordinates 3 microservices

# 1. ENVIRONMENT SETUP (.env file)
INVENTORY_SERVICE_URL=http://inventory.mystore.com:8081
PAYMENT_SERVICE_URL=http://payments.mystore.com:8082  
SHIPPING_SERVICE_URL=http://shipping.mystore.com:8083
PUBLIC_URL=http://order-coordinator.mystore.com:8080

# 2. REMOTE AGENT CONNECTIONS
inventory_service = RemoteA2aAgent(
    name="inventory_checker",
    description="Checks product availability and reserves items",
    agent_card=f"{INVENTORY_SERVICE_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"
)

payment_service = RemoteA2aAgent(
    name="payment_processor", 
    description="Processes payments and handles billing",
    agent_card=f"{PAYMENT_SERVICE_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"
)

shipping_service = RemoteA2aAgent(
    name="shipping_calculator",
    description="Calculates shipping costs and arranges delivery", 
    agent_card=f"{SHIPPING_SERVICE_URL}/{AGENT_CARD_WELL_KNOWN_PATH}"
)

# 3. STATE TRACKING CALLBACK
def track_order_progress(tool, args, tool_context, tool_response):
    \"\"\"Track which services have been called for this order\"\"\"
    service_name = tool.name
    print(f"[Order Tracking] Completed: {service_name}")
    
    # Track processing steps
    if "completed_steps" not in tool_context.state:
        tool_context.state["completed_steps"] = []
    tool_context.state["completed_steps"].append(service_name)
    tool_context.state["last_service"] = service_name
    
    return tool_response

# 4. ORCHESTRATOR AGENT
root_agent = LlmAgent(
    name="order_coordinator",
    model="gemini-2.5-flash",
    instruction=\"\"\"
        You are an Order Coordinator managing e-commerce order processing.
        
        WORKFLOW:
        1. **Inventory Check**: Use inventory_checker to verify product availability
        2. **Payment Processing**: Use payment_processor to handle billing
        3. **Shipping Arrangement**: Use shipping_calculator for delivery setup
        
        DECISION LOGIC:
        - Always check inventory first before processing payment
        - Only process payment if inventory is available
        - Only arrange shipping after successful payment
        - Check state['completed_steps'] to see what's already done
        - If any step fails, stop and report the error
        
        STATE TRACKING:
        - state['last_service'] shows which service was called last
        - state['completed_steps'] shows all completed processing steps
        - Use this info to avoid duplicate calls and handle errors
    \"\"\",
    sub_agents=[inventory_service, payment_service, shipping_service],
    after_tool_callback=track_order_progress
)

# 5. USAGE FLOW
# User: "Process order for 2 laptops, customer ID 12345"
# → inventory_checker: Verifies 2 laptops available, reserves them
# → payment_processor: Charges customer 12345 for 2 laptops  
# → shipping_calculator: Arranges delivery, provides tracking number
# Result: "Order processed! Payment confirmed, shipping arranged. Tracking: ABC123"
"""

# ============================================================================
# MICROSERVICES ARCHITECTURE PATTERNS
# ============================================================================
"""
COMMON PATTERNS FOR DISTRIBUTED AGENT SYSTEMS:

1. **PIPELINE PATTERN** (Sequential processing)
   Service A → Service B → Service C → Final Result
   Use: SequentialAgent with RemoteA2aAgent sub-agents
   
2. **ORCHESTRATOR PATTERN** (Smart coordination)
   Master Agent decides which services to call based on input
   Use: LlmAgent with RemoteA2aAgent sub-agents (like this template)
   
3. **PROXY PATTERN** (Simple forwarding)
   Single remote service behind a consistent interface
   Use: Single RemoteA2aAgent as root_agent
   
4. **FAILOVER PATTERN** (Backup services)
   Try primary service, fall back to secondary if it fails
   Use: LlmAgent with logic to handle service failures

5. **LOAD BALANCING PATTERN** (Multiple identical services)
   Distribute requests across multiple instances of same service
   Use: Custom logic to select from multiple RemoteA2aAgents

CHOOSING THE RIGHT PATTERN:
- Use PIPELINE for simple, linear workflows
- Use ORCHESTRATOR for complex decision-making
- Use PROXY for wrapping single services
- Use FAILOVER for high-availability requirements
- Use LOAD BALANCING for high-traffic scenarios
"""

# ============================================================================
# DEPLOYMENT CONSIDERATIONS
# ============================================================================
"""
WHEN DEPLOYING THIS ORCHESTRATOR:

NETWORKING:
- All remote agent URLs must be accessible from orchestrator server
- Consider using internal networking for better security and performance
- Use HTTPS in production for secure communication
- Configure firewalls to allow traffic between services

MONITORING:
- Add health checks for all remote services
- Implement logging for service calls and responses
- Monitor response times and failure rates
- Set up alerts for service outages

SCALABILITY:
- Remote services can be scaled independently  
- Orchestrator can handle multiple concurrent requests
- Consider caching agent cards to reduce network calls
- Use load balancers for high-traffic remote services

SECURITY:
- Implement authentication between services
- Use API keys or JWT tokens for service-to-service communication
- Validate all inputs from remote services
- Log all service interactions for audit trails

ERROR HANDLING:
- Handle network timeouts and connection failures
- Implement retry logic for transient failures
- Provide fallback responses when services are unavailable
- Log errors with enough detail for debugging
"""

# ============================================================================
# TESTING GUIDE FOR DISTRIBUTED SYSTEMS
# ============================================================================
"""
HOW TO TEST YOUR DISTRIBUTED AGENT SYSTEM:

1. **UNIT TESTING**
   - Test each remote service individually
   - Verify agent cards are accessible at expected URLs
   - Test service responses with sample inputs
   - Validate state tracking callbacks work correctly

2. **INTEGRATION TESTING**  
   - Test orchestrator can connect to all remote services
   - Test data flows correctly between services
   - Test state persistence across service calls
   - Test error handling when services fail

3. **END-TO-END TESTING**
   - Test complete user workflows from start to finish
   - Test with realistic user inputs and edge cases
   - Test performance under load
   - Test recovery from various failure scenarios

4. **USEFUL TESTING COMMANDS**
   # Test individual service connectivity
   curl http://your-service-url/.well-known/agent_card
   
   # Test orchestrator health
   curl http://your-orchestrator-url/health
   
   # Test complete workflow
   curl -X POST http://your-orchestrator-url/run -d '{"input": "test request"}'

5. **DEBUGGING TIPS**
   - Add extensive logging in callbacks to trace execution
   - Use different log levels for different types of events
   - Monitor network traffic between services
   - Test with services running locally before deploying remotely
"""
