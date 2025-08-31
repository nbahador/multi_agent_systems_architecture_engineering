# ============================================================================
# PARALLEL-SEQUENTIAL AGENT TEMPLATE - Concurrent Processing Pipeline
# ============================================================================
# This template creates a hybrid system: agents run in parallel, then results are processed sequentially
# Perfect for: Research → Merge, Data Collection → Analysis, Multi-source → Synthesis
# Architecture: Parallel Execution → Sequential Processing → Final Output
# ============================================================================

# --- IMPORTS SECTION ---
# These libraries provide parallel processing and sequential coordination

import asyncio  # Handles running multiple tasks simultaneously
import os  # Reads environment variables from system
from contextlib import AsyncExitStack  # Manages resource cleanup when program ends
from dotenv import load_dotenv  # Loads secrets and config from .env file
from google.adk.agents.llm_agent import LlmAgent  # Creates individual AI agents
from google.adk.agents.parallel_agent import ParallelAgent  # Runs multiple agents at the same time
from google.adk.agents.sequential_agent import SequentialAgent  # Runs agents one after another
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset  # External tools and APIs
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams  # Tool connection settings
import logging   # Prints debug and status messages
import nest_asyncio   # Allows async code in Jupyter notebooks
from toolbox_core import ToolboxSyncClient  # Connects to toolbox databases

# ============================================================================
# ENVIRONMENT SETUP - LOADS CONFIGURATION FROM .env FILE
# ============================================================================

# Load all secrets and URLs from .env file in your project folder
load_dotenv()
# IMPORTANT: This must run before using any os.environ.get() calls

# Configure logging to see what's happening during execution
logging.basicConfig(level=logging.INFO)  # INFO level shows important events only
log = logging.getLogger(__name__)  # Creates logger specific to this file

# ============================================================================
# GLOBAL VARIABLES - CONTAINERS FOR MAIN SYSTEM COMPONENTS
# ============================================================================

# --- Initialize core components as None (will be configured later) ---
root_agent: LlmAgent | None = None  # Will hold your complete agent system
exit_stack: AsyncExitStack | None = None  # Will manage cleanup when program shuts down

# ============================================================================
# CONFIGURATION SECTION - CUSTOMIZE URLS AND CONNECTIONS
# ============================================================================

# --- TOOL SERVER CONFIGURATION ---
# TODO: Set your first tool server URL (typically API-based tools)
API_TOOLS_URL = os.environ.get("API_TOOLS_URL")  # Put this URL in your .env file

# TODO: Set your second tool server URL (typically function/compute tools)
FUNCTION_TOOLS_URL = os.environ.get("FUNCTION_TOOLS_URL")  # Put this URL in your .env file

# TODO: Set your public URL (where users will access this agent system)
PUBLIC_URL = os.environ.get("PUBLIC_URL")  # Put this URL in your .env file

# Print all URLs to verify they loaded correctly from environment
print(f"API_TOOLS_URL: {API_TOOLS_URL}")
print(f"FUNCTION_TOOLS_URL: {FUNCTION_TOOLS_URL}")
print(f"PUBLIC_URL: {PUBLIC_URL}")

# ============================================================================
# TOOL SETUP - CONFIGURE EXTERNAL SERVICES YOUR AGENTS CAN USE
# ============================================================================

# --- FIRST TOOLSET - API-based tools ---
# TODO: Configure your API tools (web APIs, data services, etc.)
toolFAPI = MCPToolset(
    # Connection parameters for your API tools server
    connection_params=SseServerParams(
        url=API_TOOLS_URL,  # Your API tools server URL
        headers={}  # Add authentication headers if needed: {"Authorization": "Bearer token"}
    )
)

# --- SECOND TOOLSET - Function/compute tools ---  
# TODO: Configure your function tools (calculations, processing, etc.)
toolFunction = MCPToolset(
    # Connection parameters for your function tools server
    connection_params=SseServerParams(
        url=FUNCTION_TOOLS_URL,  # Your function tools server URL
        headers={}  # Add authentication headers if needed
    )
)

# TODO: Add more toolsets if you have additional tool servers
# Example:
# database_tools = MCPToolset(
#     connection_params=SseServerParams(url=DATABASE_TOOLS_URL, headers={})
# )

# ============================================================================
# PARALLEL AGENTS - THESE RUN SIMULTANEOUSLY TO GATHER DIFFERENT DATA
# ============================================================================

# --- FIRST PARALLEL AGENT - Data Collector 1 ---
# TODO: Replace with your first parallel worker
first_parallel_agent = LlmAgent(
    # TODO: Choose AI model for this agent
    model='gemini-2.5-flash',
    
    # TODO: Name this agent based on what it collects/processes
    name='data_collector_1',  # Change to match your use case
    
    # TODO: Write specific instructions for what this agent should do in parallel
    instruction="""
        REPLACE THIS WITH YOUR FIRST PARALLEL AGENT'S JOB
        
        This agent runs at the same time as other parallel agents.
        It should focus on ONE specific task that can be done independently.
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a data collector specializing in source A. Your job is to:
        1. Take the input query provided
        2. Use the 'search_api_source' tool to gather data from your designated source
        3. Return the raw data results clearly and concisely
        4. Focus on completeness - get all relevant information from your source
    """,
    
    # TODO: Assign tools this agent needs (choose from toolsets above)
    tools=[toolFAPI]  # This agent uses API tools
)

# --- SECOND PARALLEL AGENT - Data Collector 2 ---
# TODO: Replace with your second parallel worker  
second_parallel_agent = LlmAgent(
    # TODO: Choose AI model for this agent
    model='gemini-2.5-flash',
    
    # TODO: Name this agent based on what it collects/processes
    name='data_collector_2',  # Change to match your use case
    
    # TODO: Write specific instructions for what this agent should do in parallel
    instruction="""
        REPLACE THIS WITH YOUR SECOND PARALLEL AGENT'S JOB
        
        This agent runs simultaneously with other parallel agents.
        It should handle a DIFFERENT task that complements the first agent.
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a data collector specializing in source B. Your job is to:
        1. Take the input query provided  
        2. Use the 'calculate_metrics' tool to generate numerical analysis
        3. You MUST call the tool with a 'base_value' of 20
        4. Return the calculation results clearly and concisely
    """,
    
    # TODO: Assign tools this agent needs
    tools=[toolFunction],  # This agent uses function tools
)

# TODO: Add more parallel agents if you need additional concurrent processing
# Example third parallel agent:
# third_parallel_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='data_collector_3', 
#     instruction="You handle source C data collection...",
#     tools=[database_tools]
# )

# ============================================================================
# PARALLEL COORDINATION - GROUPS AGENTS THAT RUN SIMULTANEOUSLY  
# ============================================================================

# TODO: Configure which agents run in parallel
parallel_group = ParallelAgent(
    # TODO: Name your parallel processing group
    name='parallel_data_collectors',  # Change to describe what these agents do together
    
    # TODO: List all agents that should run at the same time
    sub_agents=[
        first_parallel_agent,   # Runs simultaneously with second_parallel_agent
        second_parallel_agent   # Runs simultaneously with first_parallel_agent
        # Add more parallel agents here if needed
    ],
    
    # NOTE: All agents in this group will start at the same time
    # Each gets the same input, but they work independently
    # Results from all agents are collected before moving to next step
)

# ============================================================================
# SEQUENTIAL PROCESSOR - HANDLES PARALLEL RESULTS
# ============================================================================

# --- RESULTS PROCESSOR - Handles output from parallel agents ---
# TODO: Replace with your results processing logic
results_processor = LlmAgent(
    # TODO: Choose AI model for processing results
    model='gemini-2.5-flash',
    
    # TODO: Name this agent based on its processing role
    name='results_synthesizer',  # Change to match what it does with parallel results
    
    # TODO: Write instructions for processing parallel agent outputs
    instruction="""
        REPLACE THIS WITH YOUR RESULTS PROCESSING LOGIC
        
        You receive combined output from all parallel agents that just finished.
        Your job is to synthesize, analyze, and format these results.
        
        EXAMPLE INSTRUCTIONS (replace with your own):
        You are a results synthesizer. Your job is to:
        
        1. **Analyze Input**: Read the complete text from the parallel processing step
        2. **Extract Data**: Find and extract all important data points from the text
        3. **Calculate Results**: Sum, average, or combine the data as appropriate
        4. **Create Summary**: Generate a comprehensive summary of findings
        5. **Format Output**: Present results in a clear, user-friendly format
        
        SPECIFIC EXAMPLE:
        If you receive "Source A found 45 items... Source B calculated 67 points...",
        extract 45 and 67, calculate total (112), and create a summary report.
    """,
    
    # TODO: Assign tools this processor needs
    tools=[toolFunction],  # This agent uses function tools for processing
)

# TODO: Add more sequential processors if you need multi-step processing
# Example additional processor:
# final_formatter = LlmAgent(
#     model='gemini-2.5-flash',
#     name='output_formatter',
#     instruction="Format the synthesized results for final presentation...",
#     tools=[toolFunction]
# )

# ============================================================================
# ROOT AGENT - ORCHESTRATES PARALLEL + SEQUENTIAL WORKFLOW
# ============================================================================

# TODO: Configure your complete system architecture
root_agent = SequentialAgent(
    # TODO: Name your complete agent system
    name="parallel_processing_system",  # Change to describe your system's purpose
    
    # TODO: Define the workflow - parallel group first, then sequential processors
    sub_agents=[
        parallel_group,      # Step 1: Run multiple agents simultaneously
        results_processor    # Step 2: Process all parallel results together
        # Add more sequential steps here if needed
    ],
    
    # TODO: Add description of what your complete system accomplishes
    description="Runs parallel data collection followed by sequential result synthesis"
)

# ============================================================================
# ALTERNATIVE ARCHITECTURES - CHOOSE WHAT FITS YOUR NEEDS
# ============================================================================

# TODO: Use this pattern for multiple parallel stages with processing between each
# root_agent = SequentialAgent(
#     name="multi_stage_parallel_system",
#     sub_agents=[
#         ParallelAgent(name="stage1", sub_agents=[agent1, agent2]),  # First parallel stage
#         results_processor,                                           # Process stage 1 results
#         ParallelAgent(name="stage2", sub_agents=[agent3, agent4]),  # Second parallel stage  
#         final_formatter                                             # Process stage 2 results
#     ]
# )

# TODO: Use this pattern for simple all-parallel processing (no sequential step)
# root_agent = ParallelAgent(
#     name="pure_parallel_system",
#     sub_agents=[first_parallel_agent, second_parallel_agent, results_processor]
# )

# TODO: Use this pattern for complex nested parallel-sequential workflows
# from google.adk.agents.loop_agent import LoopAgent
# root_agent = LoopAgent(
#     name="iterative_parallel_system",
#     sub_agents=[parallel_group, results_processor],
#     max_iterations=3  # Repeat parallel→sequential cycle 3 times
# )

# ============================================================================
# SERVER DEPLOYMENT - EXPOSE YOUR SYSTEM AS A WEB API
# ============================================================================

# Import the agent-to-API converter
from agent_to_a2a import to_a2a

# This section runs when you execute the file directly
if __name__ == "__main__":
    import uvicorn  # Fast Python web server
    
    # TODO: Customize server deployment settings
    SERVER_PORT = 8080  # Change if you need a different port number
    SERVER_HOST = '0.0.0.0'  # '0.0.0.0' accepts connections from anywhere
    
    # Convert your agent system into a web API
    a2a_app = to_a2a(
        root_agent,        # Your complete parallel-sequential system
        port=SERVER_PORT,  # Port number for the API server
        public_url=PUBLIC_URL  # Public URL from environment variables
    )
    
    # Start the web server (your parallel processing system is now live!)
    uvicorn.run(a2a_app, host=SERVER_HOST, port=SERVER_PORT)
    # Users can now send requests that trigger parallel processing

# ============================================================================
# ENVIRONMENT VARIABLES SETUP (.env file)
# ============================================================================
"""
Create a '.env' file in your project folder with these variables:
(Replace example URLs with your actual tool server URLs)

# First tool server (typically API-based tools and data sources)
API_TOOLS_URL=http://api-tools.mycompany.com

# Second tool server (typically computation and processing tools)
FUNCTION_TOOLS_URL=http://function-tools.mycompany.com

# Public URL where users can access your parallel processing system
PUBLIC_URL=http://parallel-processor.mycompany.com

# Add any additional environment variables your tools or agents need:
# DATABASE_CONNECTION_STRING=postgresql://user:pass@host:5432/db
# EXTERNAL_API_KEY=your-api-key-for-external-services
# REDIS_URL=redis://your-redis-server:6379
"""

# ============================================================================
# STEP-BY-STEP CUSTOMIZATION GUIDE
# ============================================================================
"""
TO CUSTOMIZE THIS TEMPLATE FOR YOUR PARALLEL PROCESSING SYSTEM:

□ 1. UNDERSTAND THE ARCHITECTURE
   ✓ Parallel agents run simultaneously (faster processing)
   ✓ Sequential processor combines all parallel results
   ✓ Final output synthesizes everything into coherent response
   ✓ Great for tasks that can be split into independent parts

□ 2. PLAN YOUR PARALLEL TASKS
   ✓ Identify tasks that can run independently at the same time
   ✓ Ensure each parallel agent has distinct, non-overlapping responsibilities
   ✓ Plan how results will be combined in the sequential step
   ✓ Consider what tools each parallel agent needs

□ 3. CONFIGURE ENVIRONMENT
   ✓ Set up your tool servers (API_TOOLS_URL, FUNCTION_TOOLS_URL)
   ✓ Create .env file with all necessary URLs and secrets
   ✓ Test that environment variables load correctly
   ✓ Verify all tool servers are accessible

□ 4. CUSTOMIZE PARALLEL AGENTS
   ✓ Replace first_parallel_agent with your first concurrent task
   ✓ Replace second_parallel_agent with your second concurrent task
   ✓ Add more parallel agents if you need additional concurrent processing
   ✓ Assign appropriate tools to each agent based on their tasks

□ 5. DESIGN RESULTS PROCESSOR
   ✓ Write logic to handle combined output from all parallel agents
   ✓ Implement data extraction, calculation, and synthesis logic
   ✓ Design final output format that users will receive
   ✓ Add error handling for cases where parallel agents fail

□ 6. TEST AND OPTIMIZE
   ✓ Test each parallel agent individually
   ✓ Test parallel execution with multiple agents
   ✓ Test results processing with sample parallel outputs
   ✓ Measure performance improvement from parallel processing

□ 7. DEPLOY AND MONITOR
   ✓ Deploy system with appropriate server resources
   ✓ Monitor parallel processing performance
   ✓ Set up logging to track execution times
   ✓ Configure error handling for network issues
"""

# ============================================================================
# COMPLETE EXAMPLE - MARKET RESEARCH ANALYSIS SYSTEM
# ============================================================================
"""
Here's a real example: A market research system that gathers data from multiple sources in parallel

# 1. ENVIRONMENT SETUP (.env file)
API_TOOLS_URL=http://data-apis.research.com:8081
FUNCTION_TOOLS_URL=http://analysis-tools.research.com:8082
PUBLIC_URL=http://market-research.research.com:8080

# 2. TOOL CONFIGURATION
api_tools = MCPToolset(
    connection_params=SseServerParams(url=API_TOOLS_URL, headers={})
)
analysis_tools = MCPToolset(
    connection_params=SseServerParams(url=FUNCTION_TOOLS_URL, headers={})
)

# 3. PARALLEL AGENTS - Data Collectors
competitor_researcher = LlmAgent(
    model='gemini-2.5-flash',
    name='competitor_analyst',
    instruction=\"\"\"
        You are a competitor research specialist. Your job is to:
        1. Take the company/product name from user input
        2. Use the 'analyze_competitors' tool to gather competitor data
        3. Use the 'get_market_share' tool to find market positioning
        4. Return comprehensive competitor analysis with key metrics
        5. Focus on pricing, features, and market position
    \"\"\",
    tools=[api_tools]
)

social_researcher = LlmAgent(
    model='gemini-2.5-flash',
    name='social_media_analyst', 
    instruction=\"\"\"
        You are a social media research specialist. Your job is to:
        1. Take the company/product name from user input
        2. Use the 'social_sentiment_analysis' tool to gauge public opinion
        3. You MUST call it with a 'sample_size' parameter of 1000
        4. Return social media insights, sentiment scores, and trending topics
        5. Focus on customer opinions, complaints, and praise
    \"\"\",
    tools=[analysis_tools]
)

# 4. PARALLEL GROUP - Runs both researchers simultaneously
research_team = ParallelAgent(
    name='market_research_team',
    sub_agents=[competitor_researcher, social_researcher]
)

# 5. SEQUENTIAL PROCESSOR - Combines parallel results
market_synthesizer = LlmAgent(
    model='gemini-2.5-flash',
    name='market_report_generator',
    instruction=\"\"\"
        You are a Market Research Synthesizer. Your job is to:
        
        1. **Analyze Combined Input**: Read all research data from the parallel team
        2. **Extract Key Metrics**: Find competitor data, social sentiment scores, market share numbers
        3. **Calculate Insights**: Use the 'generate_insights' tool to create strategic recommendations  
        4. **Create Report**: Synthesize everything into a comprehensive market research report
        5. **Format Output**: Present findings with clear sections: Competition, Public Opinion, Recommendations
        
        The final report should be actionable and highlight opportunities and threats.
    \"\"\",
    tools=[analysis_tools]
)

# 6. ROOT SYSTEM - Complete Market Research Pipeline
root_agent = SequentialAgent(
    name="market_research_system",
    sub_agents=[research_team, market_synthesizer],
    description="Conducts parallel market research and synthesizes comprehensive reports"
)

# 7. USAGE FLOW
# User: "Research the market for electric vehicles"
# → competitor_researcher: Analyzes EV competitors (Tesla, Ford, etc.)
# → social_researcher: Analyzes social sentiment about EVs  
# (Both run at the same time - parallel processing)
# → market_synthesizer: Combines both analyses into final report
# Result: "Market Research Report: EV market dominated by Tesla (45% share), 
#          positive social sentiment (78% favorable), key opportunity in affordable segment..."
"""

# ============================================================================
# USE CASE PATTERNS FOR PARALLEL-SEQUENTIAL SYSTEMS
# ============================================================================
"""
IDEAL USE CASES FOR THIS TEMPLATE:

1. **MULTI-SOURCE DATA GATHERING**
   Parallel: API 1 + API 2 + API 3 → Sequential: Data merger + Report generator
   Example: Stock prices + News + Social sentiment → Investment recommendation

2. **CONCURRENT ANALYSIS TASKS**  
   Parallel: Text analysis + Image analysis + Audio analysis → Sequential: Multi-modal synthesis
   Example: Analyze video content from multiple angles → Comprehensive content report

3. **DISTRIBUTED RESEARCH**
   Parallel: Academic sources + News sources + Expert opinions → Sequential: Literature review
   Example: Research scientific topic from multiple databases → Synthesized research paper

4. **PERFORMANCE OPTIMIZATION**
   Parallel: Speed test + Load test + Security scan → Sequential: Performance report
   Example: Website analysis from multiple angles → Complete performance audit

5. **CONTENT CREATION PIPELINE**
   Parallel: Topic research + Trend analysis + Competitor content → Sequential: Content strategy
   Example: Blog topic research from multiple sources → Complete content calendar

WHEN TO USE PARALLEL-SEQUENTIAL:
✓ When you have independent tasks that can run simultaneously
✓ When combining results requires intelligent synthesis  
✓ When you want to reduce total processing time
✓ When different data sources need different handling approaches

WHEN NOT TO USE:
✗ When tasks depend on each other's outputs
✗ When you only have one task to perform
✗ When parallel processing doesn't improve performance
✗ When synthesis step is simple concatenation
"""

# ============================================================================
# PERFORMANCE AND ARCHITECTURE CONSIDERATIONS
# ============================================================================
"""
OPTIMIZING YOUR PARALLEL-SEQUENTIAL SYSTEM:

PERFORMANCE BENEFITS:
- Parallel agents run simultaneously, reducing total time
- Independent tool servers can handle concurrent requests
- Network latency overlaps instead of stacking
- CPU/GPU resources used more efficiently

RESOURCE PLANNING:
- Each parallel agent needs dedicated resources
- Tool servers should handle concurrent connections
- Monitor memory usage with multiple agents running
- Plan network bandwidth for simultaneous API calls

SCALABILITY PATTERNS:
- Add more parallel agents to increase data gathering scope
- Scale tool servers independently based on usage patterns  
- Use load balancers for high-traffic tool endpoints
- Consider caching for frequently accessed data

ERROR HANDLING STRATEGIES:
- Parallel agents can fail independently
- Results processor should handle partial failures gracefully
- Implement timeout handling for slow parallel agents
- Provide fallback logic when some parallel agents fail

MONITORING AND DEBUGGING:
- Log start/completion times for each parallel agent
- Track which agents complete successfully vs fail
- Monitor tool server response times under parallel load
- Use unique request IDs to trace execution flows
"""

# ============================================================================
# TESTING STRATEGIES FOR PARALLEL SYSTEMS
# ============================================================================
"""
HOW TO TEST YOUR PARALLEL-SEQUENTIAL SYSTEM:

1. **UNIT TESTING - Individual Components**
   - Test each parallel agent individually with sample inputs
   - Test results processor with mock parallel outputs
   - Test tool connections under load
   - Verify error handling for each component

2. **PARALLEL TESTING - Concurrent Execution**
   - Test all parallel agents running simultaneously
   - Verify no race conditions or resource conflicts
   - Test with varying parallel agent completion times
   - Monitor resource usage during parallel execution

3. **INTEGRATION TESTING - Complete Workflow**
   - Test end-to-end with realistic user inputs
   - Test results synthesis with actual parallel outputs
   - Test error scenarios (some parallel agents fail)
   - Verify final output quality and completeness

4. **PERFORMANCE TESTING**
   - Measure execution time: parallel vs sequential
   - Test with different numbers of parallel agents
   - Monitor tool server performance under concurrent load
   - Identify bottlenecks and optimization opportunities

5. **USEFUL TESTING COMMANDS**
   # Test individual parallel agent
   curl -X POST http://localhost:8080/test_parallel_agent -d '{"input": "test"}'
   
   # Test complete parallel workflow
   curl -X POST http://localhost:8080/run -d '{"query": "comprehensive test"}'
   
   # Monitor parallel execution times
   time curl -X POST http://localhost:8080/run -d '{"input": "performance test"}'

6. **DEBUGGING PARALLEL SYSTEMS**
   - Add timestamps to all log messages
   - Use unique IDs to track each parallel execution
   - Log when parallel agents start and complete
   - Monitor for agents that consistently take longer
   - Check for network timeouts or tool server overload
"""
