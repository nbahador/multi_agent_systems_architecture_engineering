# =====================================
# FUNCTION-BASED MCP SERVER TEMPLATE
# =====================================
# This template helps you create an MCP server that exposes Python functions
# as tools that AI assistants can use. Perfect for calculations, data processing,
# and business logic that doesn't require external APIs.

import asyncio
import json
import uvicorn
import os
from dotenv import load_dotenv
from mcp import types as mcp_types 
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

# =====================================
# ENVIRONMENT CONFIGURATION
# =====================================
# Load environment variables from .env file
load_dotenv()

# CUSTOMIZE: Set your server host and port
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")  # Server host (usually keep as 0.0.0.0)
APP_PORT = os.environ.get("APP_PORT", 8080)       # Server port (change if needed)

# ADD MORE: Include any additional environment variables you need
# API_KEY = os.environ.get("API_KEY")               # Example: API keys
# DATABASE_URL = os.environ.get("DATABASE_URL")     # Example: Database connections
# SECRET_KEY = os.environ.get("SECRET_KEY")         # Example: Security keys

# =====================================
# FUNCTION DEFINITIONS SECTION
# =====================================
# REPLACE ALL FUNCTIONS BELOW: Create your own business logic functions
# Each function should:
# 1. Have clear parameters with type hints
# 2. Include a detailed docstring
# 3. Return a string result
# 4. Handle errors gracefully

def your_calculation_function(input_value: int) -> str:
    """
    REPLACE: Write your function description here.
    
    This function should describe exactly what it does and when to use it.
    The AI assistant will read this to understand when to call this function.
    
    Args:
        input_value: REPLACE - Describe what this parameter is for
        
    Returns:
        str: REPLACE - Describe what the function returns
        
    Example: "Calculates compound interest on an investment amount"
    """
    try:
        # REPLACE: Add your calculation or business logic here
        # Examples of what you can do:
        # - Mathematical calculations: result = input_value ** 2
        # - Data transformations: processed_data = transform(input_value)
        # - File operations: content = read_file(input_value)
        # - String processing: formatted = format_text(input_value)
        
        # Example calculation:
        result = input_value * 2  # Replace with your logic
        
        # CUSTOMIZE: Return a meaningful success message
        return f"Calculation completed successfully! Result: {result}"
        
    except Exception as e:
        # CUSTOMIZE: Return a meaningful error message
        return f"Calculation failed. Error: {str(e)}"


def your_processing_function(text_input: str, multiplier: int) -> str:
    """
    REPLACE: Another function example with multiple parameters.
    
    This function demonstrates how to handle multiple input parameters
    and perform more complex processing operations.
    
    Args:
        text_input: REPLACE - Describe the text parameter
        multiplier: REPLACE - Describe the numeric parameter
        
    Returns:
        str: REPLACE - Describe the return value
        
    Example: "Processes text data and applies formatting rules"
    """
    try:
        # REPLACE: Add your processing logic here
        # Examples:
        # - Text processing: result = text_input.upper()
        # - Data validation: if validate(text_input): ...
        # - Complex calculations: score = calculate_score(text_input, multiplier)
        # - Data formatting: formatted = format_output(text_input, multiplier)
        
        # Example processing:
        processed_text = text_input * multiplier  # Replace with your logic
        
        # CUSTOMIZE: Return your processed result
        return f"Text processing completed! Processed: {processed_text}"
        
    except Exception as e:
        # CUSTOMIZE: Handle errors appropriately
        return f"Text processing failed. Error: {str(e)}"


def your_data_function(data_list: list) -> str:
    """
    REPLACE: Function that works with lists or complex data.
    
    This function shows how to handle more complex data types
    like lists, dictionaries, or custom objects.
    
    Args:
        data_list: REPLACE - Describe the list parameter
        
    Returns:
        str: REPLACE - Describe what analysis is returned
        
    Example: "Analyzes a list of sales data and returns summary statistics"
    """
    try:
        # REPLACE: Add your data processing logic here
        # Examples:
        # - List analysis: average = sum(data_list) / len(data_list)
        # - Data filtering: filtered = [x for x in data_list if x > threshold]
        # - Statistical analysis: stats = calculate_statistics(data_list)
        # - Data aggregation: summary = aggregate_data(data_list)
        
        # Example analysis:
        if not data_list:
            return "No data provided for analysis."
        
        total = sum(data_list)
        average = total / len(data_list)
        maximum = max(data_list)
        minimum = min(data_list)
        
        # CUSTOMIZE: Return your analysis results
        return f"Data analysis complete! Total: {total}, Average: {average:.2f}, Max: {maximum}, Min: {minimum}"
        
    except Exception as e:
        # CUSTOMIZE: Handle data processing errors
        return f"Data analysis failed. Error: {str(e)}"

# ADD MORE FUNCTIONS: Copy the patterns above to create additional functions
# def your_fourth_function(param1: str) -> str:
#     """Your fourth function description."""
#     try:
#         # Your implementation here
#         result = process_data(param1)
#         return f"Success: {result}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# =====================================
# TOOL REGISTRATION SECTION
# =====================================
# REPLACE: Create FunctionTool instances for each of your functions
# The variable name should be descriptive and end with "Tool"

your_calculation_functionTool = FunctionTool(your_calculation_function)
your_processing_functionTool = FunctionTool(your_processing_function)
your_data_functionTool = FunctionTool(your_data_function)

# ADD MORE TOOLS: Create tool instances for additional functions
# your_fourth_functionTool = FunctionTool(your_fourth_function)

# REGISTER ALL TOOLS: Add your tools to this dictionary
# Key = tool name, Value = tool instance
available_tools = {
    your_calculation_functionTool.name: your_calculation_functionTool,
    your_processing_functionTool.name: your_processing_functionTool,
    your_data_functionTool.name: your_data_functionTool,
    # ADD MORE: your_fourth_functionTool.name: your_fourth_functionTool,
}

# =====================================
# MCP SERVER SETUP SECTION
# =====================================
# CUSTOMIZE: Change the server name to describe your server's purpose
app = Server("Your-Function-Server")  # Replace with a descriptive name
sse = SseServerTransport("/messages/")

@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """
    MCP handler to list available tools.
    DO NOT MODIFY: This function tells AI assistants what tools are available.
    """
    # Convert all tools to MCP format
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
    DO NOT MODIFY: This function executes tools when called by AI assistants.
    """
    print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")

    # Look up the tool by name in our registry
    tool_to_call = available_tools.get(name)
    if tool_to_call:
        try:
            # Execute the function tool
            adk_response = await tool_to_call.run_async(
                args=arguments,
                tool_context=None,  # No ADK context needed for function tools
            )
            print(f"MCP Server: Tool '{name}' executed successfully.")
            
            # Return the response as MCP text content
            response_text = json.dumps(adk_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            print(f"MCP Server: Error executing tool '{name}': {e}")
            # Return error as JSON
            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        # Handle calls to unknown tools
        print(f"MCP Server: Tool '{name}' not found.")
        error_text = json.dumps({"error": f"Tool '{name}' not implemented."})
        return [mcp_types.TextContent(type="text", text=error_text)]

# =====================================
# SERVER TRANSPORT SECTION
# =====================================
# DO NOT MODIFY: This section handles the MCP communication protocol

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
    debug=True,  # CUSTOMIZE: Set to False in production
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

# =====================================
# SERVER STARTUP SECTION
# =====================================
# CUSTOMIZE: You can modify the startup messages but keep the core logic

if __name__ == "__main__":
    # CUSTOMIZE: Update these startup messages to match your server
    print("🚀 Launching Your Function-Based MCP Server...")
    print(f"📡 Server will run on {APP_HOST}:{APP_PORT}")
    print(f"🔧 Available tools: {list(available_tools.keys())}")
    print(f"📋 Total functions exposed: {len(available_tools)}")
    
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
# FUNCTION TYPES REFERENCE GUIDE
# =====================================
"""
PARAMETER TYPES YOU CAN USE:
===========================
- int: Whole numbers (1, 42, -5)
- float: Decimal numbers (3.14, -2.5, 0.0)
- str: Text strings ("hello", "file.txt")
- bool: True/False values
- list: Lists of items ([1, 2, 3], ["a", "b", "c"])
- dict: Key-value pairs ({"name": "John", "age": 30})

RETURN TYPE:
============
Always return str: Your functions should always return a string message
that describes the result or any errors that occurred.
"""

# =====================================
# COMPLETE EXAMPLES: BUSINESS FUNCTIONS
# =====================================
"""
EXAMPLE 1: FINANCIAL CALCULATOR SERVER
=====================================

def calculate_compound_interest(principal: float, rate: float, time: int, compounds_per_year: int) -> str:
    '''Calculates compound interest for investments.'''
    try:
        amount = principal * (1 + rate/compounds_per_year) ** (compounds_per_year * time)
        interest = amount - principal
        return f"Investment Result: Principal ${principal:,.2f}, Final Amount ${amount:,.2f}, Interest Earned ${interest:,.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def calculate_loan_payment(loan_amount: float, annual_rate: float, years: int) -> str:
    '''Calculates monthly payment for a loan.'''
    try:
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        if monthly_rate == 0:
            payment = loan_amount / num_payments
        else:
            payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        total_paid = payment * num_payments
        total_interest = total_paid - loan_amount
        return f"Loan Payment: ${payment:.2f}/month, Total Paid: ${total_paid:,.2f}, Total Interest: ${total_interest:,.2f}"
    except Exception as e:
        return f"Loan calculation error: {str(e)}"

def calculate_retirement_savings(monthly_contribution: float, annual_return: float, years: int) -> str:
    '''Calculates retirement savings projection.'''
    try:
        monthly_return = annual_return / 12
        months = years * 12
        if monthly_return == 0:
            total = monthly_contribution * months
        else:
            total = monthly_contribution * (((1 + monthly_return)**months - 1) / monthly_return)
        contributed = monthly_contribution * months
        gains = total - contributed
        return f"Retirement Projection: Total Savings ${total:,.2f}, Contributions ${contributed:,.2f}, Investment Gains ${gains:,.2f}"
    except Exception as e:
        return f"Retirement calculation error: {str(e)}"

# Tool Registration:
calculate_compound_interestTool = FunctionTool(calculate_compound_interest)
calculate_loan_paymentTool = FunctionTool(calculate_loan_payment)
calculate_retirement_savingsTool = FunctionTool(calculate_retirement_savings)

available_tools = {
    calculate_compound_interestTool.name: calculate_compound_interestTool,
    calculate_loan_paymentTool.name: calculate_loan_paymentTool,
    calculate_retirement_savingsTool.name: calculate_retirement_savingsTool,
}

# Server Name:
app = Server("Financial-Calculator-Server")

EXAMPLE 2: TEXT PROCESSING SERVER
================================

def analyze_text_sentiment(text: str) -> str:
    '''Analyzes the sentiment of provided text.'''
    try:
        # Simple sentiment analysis (replace with actual NLP library)
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing', 'poor']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "Positive"
        elif negative_count > positive_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
            
        return f"Sentiment Analysis: {sentiment} (Positive words: {positive_count}, Negative words: {negative_count})"
    except Exception as e:
        return f"Sentiment analysis error: {str(e)}"

def count_words_and_chars(text: str) -> str:
    '''Counts words, characters, and provides text statistics.'''
    try:
        word_count = len(text.split())
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        return f"Text Statistics: {word_count} words, {char_count} characters, {char_count_no_spaces} chars (no spaces), {sentence_count} sentences"
    except Exception as e:
        return f"Text analysis error: {str(e)}"

def format_text_case(text: str, case_type: str) -> str:
    '''Formats text in different cases (upper, lower, title, sentence).'''
    try:
        case_type = case_type.lower()
        
        if case_type == "upper":
            result = text.upper()
        elif case_type == "lower":
            result = text.lower()
        elif case_type == "title":
            result = text.title()
        elif case_type == "sentence":
            result = text.capitalize()
        else:
            return f"Invalid case type. Use: upper, lower, title, or sentence"
            
        return f"Text formatted as {case_type}: {result}"
    except Exception as e:
        return f"Text formatting error: {str(e)}"

EXAMPLE 3: DATA VALIDATION SERVER
===============================

def validate_email(email: str) -> str:
    '''Validates if an email address is properly formatted.'''
    try:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            return f"✅ Email '{email}' is valid"
        else:
            return f"❌ Email '{email}' is not valid"
    except Exception as e:
        return f"Email validation error: {str(e)}"

def validate_phone_number(phone: str, country_code: str) -> str:
    '''Validates phone number format for different countries.'''
    try:
        import re
        
        # Remove all non-digit characters
        digits_only = re.sub(r'[^\d]', '', phone)
        
        patterns = {
            'US': r'^\d{10}$',           # 10 digits for US
            'UK': r'^\d{11}$',           # 11 digits for UK
            'CA': r'^\d{10}$',           # 10 digits for Canada
        }
        
        pattern = patterns.get(country_code.upper())
        if not pattern:
            return f"❌ Unsupported country code: {country_code}"
            
        if re.match(pattern, digits_only):
            return f"✅ Phone number '{phone}' is valid for {country_code}"
        else:
            return f"❌ Phone number '{phone}' is not valid for {country_code}"
    except Exception as e:
        return f"Phone validation error: {str(e)}"

def validate_credit_card(card_number: str) -> str:
    '''Validates credit card number using Luhn algorithm.'''
    try:
        import re
        
        # Remove spaces and dashes
        card_number = re.sub(r'[^\d]', '', card_number)
        
        # Basic length check
        if len(card_number) < 13 or len(card_number) > 19:
            return f"❌ Credit card number must be 13-19 digits"
        
        # Luhn algorithm
        def luhn_check(card_num):
            digits = [int(d) for d in card_num]
            for i in range(len(digits) - 2, -1, -2):
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
            return sum(digits) % 10 == 0
        
        if luhn_check(card_number):
            return f"✅ Credit card number is valid (Luhn check passed)"
        else:
            return f"❌ Credit card number is invalid (Luhn check failed)"
    except Exception as e:
        return f"Credit card validation error: {str(e)}"
"""

# =====================================
# CUSTOMIZATION CHECKLIST
# =====================================
"""
STEP-BY-STEP CUSTOMIZATION GUIDE:
=================================

1. ENVIRONMENT SETUP:
   □ Create .env file with APP_HOST and APP_PORT
   □ Add any additional environment variables you need
   □ Install required dependencies: pip install uvicorn python-dotenv

2. FUNCTION REPLACEMENT:
   □ Replace all example functions with your own business logic
   □ Update function names to be descriptive
   □ Write clear docstrings explaining what each function does
   □ Add proper parameter type hints
   □ Include error handling in each function

3. TOOL REGISTRATION:
   □ Create FunctionTool instances for each function
   □ Update tool variable names to match your functions
   □ Add all tools to the available_tools dictionary
   □ Remove any unused tool registrations

4. SERVER CONFIGURATION:
   □ Change the server name in Server() constructor
   □ Update startup messages to reflect your server's purpose
   □ Modify APP_PORT if you need a different port

5. TESTING:
   □ Test each function individually
   □ Verify the server starts without errors
   □ Test tool listing endpoint
   □ Test tool execution with sample parameters

COMMON FUNCTION PATTERNS:
========================

CALCULATION FUNCTIONS:
- Mathematical operations (interest, taxes, conversions)
- Statistical analysis (averages, trends, forecasts)
- Engineering calculations (physics, chemistry formulas)

PROCESSING FUNCTIONS: 
- Text manipulation (formatting, parsing, cleaning)
- Data transformation (JSON processing, CSV handling)
- Image processing (resize, format conversion)

VALIDATION FUNCTIONS:
- Input validation (emails, phone numbers, IDs)
- Data integrity checks (checksums, format verification)
- Business rule validation (price ranges, date limits)

UTILITY FUNCTIONS:
- Date/time operations (formatting, calculations, timezones)
- File operations (reading, writing, processing)
- String operations (encoding, hashing, templating)

ENVIRONMENT VARIABLES TO SET:
============================
Create a .env file with:

# Server Configuration
APP_HOST=0.0.0.0
APP_PORT=8080

# Add your own variables as needed:
# API_KEY=your_api_key_here
# DATABASE_URL=your_database_url
# SECRET_KEY=your_secret_key
# MAX_PROCESSING_SIZE=1000000
"""

# =====================================
# DEPENDENCIES INSTALLATION
# =====================================
"""
REQUIRED DEPENDENCIES:
=====================
pip install uvicorn python-dotenv starlette

OPTIONAL DEPENDENCIES (add based on your functions):
===================================================
pip install requests          # For HTTP API calls
pip install pandas           # For data processing
pip install numpy            # For numerical calculations
pip install pillow           # For image processing
pip install beautifulsoup4   # For HTML/XML parsing
pip install openpyxl         # For Excel file processing
pip install python-dateutil # For advanced date handling
pip install cryptography     # For encryption/hashing
pip install sqlalchemy      # For database operations
pip install pydantic        # For data validation
"""

# =====================================
# USAGE EXAMPLES
# =====================================
"""
HOW TO USE YOUR MCP SERVER:
==========================

1. Start your server:
   python main.py

2. Connect from an agent (in another script):
   from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
   from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams
   
   tools = MCPToolset(
       connection_params=SseServerParams(url="http://localhost:8080", headers={})
   )

3. Use in an LlmAgent:
   agent = LlmAgent(
       model='gemini-2.5-flash',
       name='my_agent',
       instruction="You can perform calculations and data processing.",
       tools=tools
   )

TESTING YOUR FUNCTIONS:
======================
Test your functions directly before deploying:

# Test calculation function
result = your_calculation_function(42)
print(result)

# Test processing function  
result = your_processing_function("hello world", 3)
print(result)

# Test data function
result = your_data_function([1, 2, 3, 4, 5])
print(result)
"""
