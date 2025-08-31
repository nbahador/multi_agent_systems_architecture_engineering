# MCP Server Template - Complete Guide
# This template helps you create your own MCP (Model Context Protocol) server
# that exposes custom tools/functions to AI assistants like Claude

import asyncio
import json
import uvicorn
import os
from dotenv import load_dotenv
import requests
from mcp import types as mcp_types 
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route

# REPLACE THIS: Import your function tool wrapper
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# =====================================
# CONFIGURATION SECTION
# =====================================
# Load environment variables from .env file
load_dotenv()

# CUSTOMIZE THESE: Set your server configuration
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")  # Server host (usually keep as 0.0.0.0)
APP_PORT = os.environ.get("APP_PORT", 8080)       # Server port (change if needed)

# REPLACE THIS: Add your API endpoint URL if you're calling external services
API_SERVER_URL = os.environ.get('API_SERVER_URL')  # Example: "https://your-api.com"

# =====================================
# FUNCTION DEFINITIONS SECTION
# =====================================
# REPLACE THESE FUNCTIONS: Define your own custom functions here
# Each function should:
# 1. Have a clear docstring describing what it does
# 2. Return a string with the result
# 3. Handle errors gracefully

def your_first_function() -> str:
    """
    REPLACE THIS: Write a description of what your function does.
    This will be shown to the AI assistant so it knows when to use this tool.
    
    Example: "Calculates the square of a number and returns the result."
    """
    try:
        # REPLACE THIS: Add your function logic here
        # Example options:
        # - Call an external API: requests.get("https://api.example.com/data")
        # - Perform calculations: result = number ** 2
        # - Read from database: db.query("SELECT * FROM table")
        # - Process files: with open("file.txt", "r") as f: content = f.read()
        
        # Example implementation:
        response = requests.post(f"{API_SERVER_URL}/your-endpoint")
        response.raise_for_status()
        data = response.json()
        
        # CUSTOMIZE THIS: Return a meaningful success message
        return f"Success! Your function returned: {data.get('result')}"
        
    except requests.exceptions.RequestException as e:
        # CUSTOMIZE THIS: Return a meaningful error message
        return f"Error: Your function failed. Reason: {e}"
    except Exception as e:
        # Handle any other errors
        return f"Unexpected error: {str(e)}"


def your_second_function(parameter1: str, parameter2: int) -> str:
    """
    REPLACE THIS: Another function example with parameters.
    
    Args:
        parameter1: Description of first parameter
        parameter2: Description of second parameter
    
    Example: "Sends a notification message to a specific user ID."
    """
    try:
        # REPLACE THIS: Add your function logic here
        # Example with parameters:
        # result = f"Processing {parameter1} with value {parameter2}"
        
        # Example API call with parameters:
        payload = {
            "message": parameter1,
            "user_id": parameter2
        }
        response = requests.post(f"{API_SERVER_URL}/send-notification", json=payload)
        response.raise_for_status()
        data = response.json()
        
        # CUSTOMIZE THIS: Return success message
        return f"Notification sent successfully! Message ID: {data.get('message_id')}"
        
    except Exception as e:
        # CUSTOMIZE THIS: Return error message
        return f"Failed to send notification. Error: {str(e)}"


# ADD MORE FUNCTIONS: Copy the pattern above to add more functions
# def your_third_function() -> str:
#     """Your third function description."""
#     # Your implementation here
#     pass

# =====================================
# TOOL REGISTRATION SECTION
# =====================================
# REPLACE THESE: Create tool instances for each of your functions
# The variable name should match your function name + "Tool"
your_first_functionTool = FunctionTool(your_first_function)
your_second_functionTool = FunctionTool(your_second_function)

# ADD MORE TOOLS: Create tool instances for additional functions
# your_third_functionTool = FunctionTool(your_third_function)

# REGISTER TOOLS: Add all your tools to this dictionary
# Key = tool name, Value = tool instance
available_tools = {
    your_first_functionTool.name: your_first_functionTool,
    your_second_functionTool.name: your_second_functionTool,
    # ADD MORE: your_third_functionTool.name: your_third_functionTool,
}

# =====================================
# MCP SERVER SETUP SECTION
# =====================================
# CUSTOMIZE THIS: Change the server name to describe your server
app = Server("Your-Custom-MCP-Server")  # Replace with your server name
sse = SseServerTransport("/messages/")

@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """
    MCP handler to list available tools.
    DO NOT MODIFY: This function tells the AI what tools are available.
    """
    # Convert each tool to MCP format
    mcp_tools = []
    for tool_name, tool_instance in available_tools.items():
        schema = adk_to_mcp_tool_type(tool_instance)
        mcp_tools.append(schema)
        print(f"MCP Server: Advertising tool: {schema.name}")
    
    print(f"MCP Server: Received list_tools request. Total tools: {len(mcp_tools)}")
    return mcp_tools

@app.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
    """
    MCP handler to execute a tool call.
    DO NOT MODIFY: This function executes the tools when called by the AI.
    """
    print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")

    # Look up the tool by name
    tool_to_call = available_tools.get(name)
    if tool_to_call:
        try:
            # Execute the tool
            adk_response = await tool_to_call.run_async(
                args=arguments,
                tool_context=None,
            )
            print(f"MCP Server: Tool '{name}' executed successfully.")
            
            # Return the response as MCP text content
            response_text = json.dumps(adk_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            print(f"MCP Server: Error executing tool '{name}': {e}")
            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # Handle unknown tools
        print(f"MCP Server: Tool '{name}' not found.")
        error_text = json.dumps({"error": f"Tool '{name}' not implemented."})
        return [mcp_types.TextContent(type="text", text=error_text)]

# =====================================
# SERVER TRANSPORT SECTION
# =====================================
# DO NOT MODIFY: This section handles the communication protocol

async def handle_sse(request):
    """Handles Server-Sent Events for MCP communication."""
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(
            streams[0], streams[1], app.create_initialization_options()
        )

# Create the Starlette ASGI application
starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

# =====================================
# SERVER STARTUP SECTION
# =====================================
# CUSTOMIZE THIS: You can modify the startup messages but keep the core logic

if __name__ == "__main__":
    print("🚀 Launching Your Custom MCP Server...")
    print(f"📡 Server will run on {APP_HOST}:{APP_PORT}")
    print(f"🔧 Available tools: {list(available_tools.keys())}")
    
    try:
        # Start the server
        asyncio.run(uvicorn.run(starlette_app, host=APP_HOST, port=APP_PORT))
    except KeyboardInterrupt:
        print("\n⏹️  MCP Server stopped by user.")
    except Exception as e:
        print(f"❌ MCP Server encountered an error: {e}")
    finally:
        print("🔚 MCP Server process exiting.")

# =====================================
# TEMPLATE USAGE EXAMPLES
# =====================================

"""
EXAMPLE 1: Weather Service MCP Server
--------------------------------------
Replace the functions above with:

def get_weather(city: str) -> str:
    '''Gets current weather for a specified city.'''
    try:
        api_key = os.environ.get('WEATHER_API_KEY')
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        description = data['weather'][0]['description']
        return f"Weather in {city}: {temp:.1f}°C, {description}"
    except Exception as e:
        return f"Failed to get weather for {city}: {str(e)}"

def get_forecast(city: str, days: int) -> str:
    '''Gets weather forecast for specified city and number of days.'''
    try:
        api_key = os.environ.get('WEATHER_API_KEY')
        response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt={days*8}&appid={api_key}")
        response.raise_for_status()
        data = response.json()
        forecast_summary = f"5-day forecast for {city}:\\n"
        for item in data['list'][::8]:  # Every 8th item (daily)
            date = item['dt_txt'].split()[0]
            temp = item['main']['temp'] - 273.15
            desc = item['weather'][0]['description']
            forecast_summary += f"{date}: {temp:.1f}°C, {desc}\\n"
        return forecast_summary
    except Exception as e:
        return f"Failed to get forecast for {city}: {str(e)}"

# Then register tools:
get_weatherTool = FunctionTool(get_weather)
get_forecastTool = FunctionTool(get_forecast)

available_tools = {
    get_weatherTool.name: get_weatherTool,
    get_forecastTool.name: get_forecastTool,
}

# Change server name:
app = Server("Weather-MCP-Server")

EXAMPLE 2: File Management MCP Server
------------------------------------
def list_files(directory: str) -> str:
    '''Lists all files in the specified directory.'''
    try:
        files = os.listdir(directory)
        return f"Files in {directory}: {', '.join(files)}"
    except Exception as e:
        return f"Error listing files: {str(e)}"

def read_file(filepath: str) -> str:
    '''Reads and returns the content of a text file.'''
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Content of {filepath}:\\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    '''Writes content to a specified file.'''
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

EXAMPLE 3: Database MCP Server
-----------------------------
import sqlite3

def query_database(sql: str) -> str:
    '''Executes a SQL query and returns the results.'''
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.close()
        return f"Query results: {results}"
    except Exception as e:
        return f"Database error: {str(e)}"

def insert_record(table: str, data: str) -> str:
    '''Inserts a new record into the specified table.'''
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table} VALUES ({data})")
        conn.commit()
        conn.close()
        return f"Record inserted into {table}"
    except Exception as e:
        return f"Insert error: {str(e)}"

SETUP INSTRUCTIONS:
==================
1. Install dependencies:
   pip install uvicorn python-dotenv requests mcp starlette

2. Create .env file with your configuration:
   APP_HOST=0.0.0.0
   APP_PORT=8080
   API_SERVER_URL=https://your-api.com
   # Add any API keys or secrets here

3. Replace the example functions with your own
4. Update the tool registration section
5. Change the server name
6. Run: python main.py

ENVIRONMENT VARIABLES TO SET:
============================
- APP_HOST: Server host address (default: 0.0.0.0)
- APP_PORT: Server port (default: 8080)
- API_SERVER_URL: External API URL if calling external services
- Add any API keys, database URLs, or other configuration here

CUSTOMIZATION CHECKLIST:
========================
□ Replace function definitions with your own
□ Update function docstrings
□ Register your tools in available_tools dictionary
□ Change server name in Server() constructor
□ Set up environment variables
□ Test your functions work correctly
□ Update startup messages if desired
"""
