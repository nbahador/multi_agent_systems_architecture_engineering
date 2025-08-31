# cooldown_plugin_template.py
"""
COOLDOWN PLUGIN TEMPLATE
========================
A reusable template for creating cooldown functionality in Google ADK agents.
This plugin prevents rapid successive actions by enforcing a waiting period.

WHAT THIS TEMPLATE DOES:
- Tracks when actions were last performed
- Enforces a cooldown period between actions
- Integrates with external APIs for cooldown state management
- Provides callbacks for agent behavior modification

HOW TO USE THIS TEMPLATE:
1. Replace all [PLACEHOLDER] sections with your specific values
2. Modify the cooldown logic in the main functions
3. Customize the API integration for your backend
4. Add your specific business logic
"""

# ===== IMPORTS SECTION =====
# These are the required imports for Google ADK plugins
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from typing import Optional
from google.genai import types
import requests
from datetime import datetime, timezone, timedelta
import os

# ===== CONFIGURATION SECTION =====
# CUSTOMIZE THESE VALUES FOR YOUR USE CASE:

# [PLACEHOLDER 1] - Cooldown Duration
# Set how long users must wait between actions (in seconds)
# Examples: 30 (30 seconds), 300 (5 minutes), 3600 (1 hour)
COOLDOWN_PERIOD_SECONDS = 60  # Replace 60 with your desired cooldown time

# [PLACEHOLDER 2] - API Endpoint
# Set your backend API URL for cooldown state management
# This should point to your server that tracks cooldown states
# Example: "https://your-api.com/cooldown" or "http://localhost:8000/api/cooldown"
COOLDOWN_API_URL = os.environ.get("API_SERVER_URL")  # Replace with your API URL
print(f"COOLDOWN_API_URL: {COOLDOWN_API_URL}")

# [PLACEHOLDER 3] - Additional Configuration
# Add any other configuration variables you need:
# COOLDOWN_MAX_RETRIES = 3  # Maximum retry attempts
# COOLDOWN_ERROR_MESSAGE = "Please wait before trying again"  # Custom error message
# COOLDOWN_BYPASS_ROLES = ["admin", "premium"]  # Roles that can bypass cooldown


class CooldownPlugin(BasePlugin):
    """
    [PLACEHOLDER 4] - Plugin Class Name and Description
    
    Replace 'CooldownPlugin' with your specific plugin name.
    Examples: RateLimitPlugin, UserThrottlePlugin, RequestCooldownPlugin
    
    This plugin manages cooldown periods for user actions to prevent abuse.
    
    WHAT YOU CAN CUSTOMIZE:
    - Plugin name and description
    - Cooldown logic and duration
    - API integration methods
    - Error handling and responses
    """
    
    def __init__(self):
        """
        Initialize the plugin.
        
        [PLACEHOLDER 5] - Initialization Logic
        Add any setup code you need here:
        - Initialize databases connections
        - Set up logging
        - Configure default values
        - Load configuration files
        """
        super().__init__()
        # Add your initialization code here
        # Example: self.logger = logging.getLogger(__name__)
        # Example: self.db_connection = connect_to_database()
    
    def on_agent_request(
        self, 
        agent: BaseAgent, 
        request: LlmRequest, 
        context: CallbackContext
    ) -> Optional[LlmRequest]:
        """
        Called when an agent receives a request. This is where cooldown logic runs.
        
        [PLACEHOLDER 6] - Request Processing Logic
        
        PARAMETERS EXPLAINED:
        - agent: The agent instance handling the request
        - request: The incoming LLM request object
        - context: Additional context and metadata
        
        RETURN VALUE:
        - Return the original request to continue processing
        - Return None to block the request
        - Return a modified request to change behavior
        
        CUSTOMIZE THIS SECTION:
        - Extract user identification (user ID, session ID, etc.)
        - Implement your cooldown checking logic
        - Add custom validation rules
        - Integrate with your specific API or database
        """
        
        # [PLACEHOLDER 7] - User Identification
        # Extract user identifier from the request
        # You might get this from headers, session data, or request context
        user_id = self._extract_user_id(request, context)  # Implement this method
        
        if not user_id:
            # [PLACEHOLDER 8] - Handle Missing User ID
            # Decide what to do when user ID cannot be determined
            # Options: allow request, block request, use default ID
            return request  # Or return None to block
        
        # [PLACEHOLDER 9] - Cooldown Check
        # Check if user is in cooldown period
        if self._is_user_in_cooldown(user_id):
            # [PLACEHOLDER 10] - Cooldown Response
            # Customize what happens when user is in cooldown
            self._handle_cooldown_violation(agent, request, context, user_id)
            return None  # Block the request
        
        # [PLACEHOLDER 11] - Record Action
        # Log that user performed an action (for future cooldown checks)
        self._record_user_action(user_id)
        
        # [PLACEHOLDER 12] - Allow Request
        # Request passes cooldown check, allow it to proceed
        return request
    
    def _extract_user_id(self, request: LlmRequest, context: CallbackContext) -> Optional[str]:
        """
        Extract user identifier from request.
        
        [PLACEHOLDER 13] - User ID Extraction Logic
        
        CUSTOMIZE THIS METHOD:
        - Define how to identify unique users
        - Extract from request headers, metadata, or context
        - Handle anonymous users vs authenticated users
        
        COMMON APPROACHES:
        - Use session ID: context.session_id
        - Use user authentication: request.headers.get('user-id')
        - Use IP address: request.client_ip
        - Use custom identifier: request.metadata.get('client_id')
        """
        
        # Example implementations (choose one or combine):
        
        # Option 1: Use session ID from context
        # return getattr(context, 'session_id', None)
        
        # Option 2: Extract from request headers
        # return request.headers.get('user-id')
        
        # Option 3: Use IP address as identifier
        # return getattr(request, 'client_ip', None)
        
        # Option 4: Custom metadata extraction
        # return request.metadata.get('user_identifier')
        
        # [REPLACE THIS] - Implement your user ID extraction logic
        return "default_user"  # Replace with actual extraction logic
    
    def _is_user_in_cooldown(self, user_id: str) -> bool:
        """
        Check if user is currently in cooldown period.
        
        [PLACEHOLDER 14] - Cooldown Check Logic
        
        CUSTOMIZE THIS METHOD:
        - Implement your cooldown checking mechanism
        - Choose between local storage, database, or API calls
        - Add custom cooldown rules (different times for different actions)
        
        IMPLEMENTATION OPTIONS:
        1. API-based checking (recommended for distributed systems)
        2. Local in-memory storage (for single-instance deployments)
        3. Database queries (for persistent storage)
        4. Redis/cache-based checking (for high performance)
        """
        
        try:
            # [PLACEHOLDER 15] - API Integration
            # Replace with your actual API endpoint and logic
            if COOLDOWN_API_URL:
                # Example API call structure:
                response = requests.get(
                    f"{COOLDOWN_API_URL}/check/{user_id}",  # Customize endpoint
                    timeout=5  # Adjust timeout as needed
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # [PLACEHOLDER 16] - API Response Processing
                    # Customize based on your API response format
                    # Example: return data.get('in_cooldown', False)
                    # Example: return data.get('time_remaining', 0) > 0
                    return data.get('in_cooldown', False)  # Replace with your logic
                
                # [PLACEHOLDER 17] - API Error Handling
                # Handle API failures gracefully
                # Options: assume no cooldown, assume cooldown, retry, etc.
                return False  # Default behavior on API failure
            
            # [PLACEHOLDER 18] - Fallback Logic
            # What to do when API is not available
            # You could implement local checking here
            return False
            
        except Exception as e:
            # [PLACEHOLDER 19] - Exception Handling
            # Handle network errors, timeouts, etc.
            print(f"Cooldown check failed: {e}")
            return False  # Default to allowing request on error
    
    def _record_user_action(self, user_id: str) -> None:
        """
        Record that user performed an action (starts cooldown timer).
        
        [PLACEHOLDER 20] - Action Recording Logic
        
        CUSTOMIZE THIS METHOD:
        - Choose how to store action timestamps
        - Implement your preferred storage mechanism
        - Add metadata about the action if needed
        
        STORAGE OPTIONS:
        1. API call to your backend
        2. Database insert/update
        3. Cache/Redis storage
        4. Local file storage
        """
        
        try:
            # [PLACEHOLDER 21] - Record Action Implementation
            if COOLDOWN_API_URL:
                # Example API call to record action:
                response = requests.post(
                    f"{COOLDOWN_API_URL}/record/{user_id}",  # Customize endpoint
                    json={
                        'timestamp': datetime.now(timezone.utc).isoformat(),
                        'action_type': 'llm_request',  # Customize action type
                        # [PLACEHOLDER 22] - Additional Metadata
                        # Add any extra data you want to track:
                        # 'request_size': len(str(request)),
                        # 'user_agent': request.headers.get('user-agent'),
                        # 'endpoint': request.endpoint,
                    },
                    timeout=5
                )
                
                if response.status_code != 200:
                    print(f"Failed to record action for user {user_id}")
            
        except Exception as e:
            # [PLACEHOLDER 23] - Recording Error Handling
            print(f"Error recording user action: {e}")
            # Decide: Should failures block the request or just log?
    
    def _handle_cooldown_violation(
        self, 
        agent: BaseAgent, 
        request: LlmRequest, 
        context: CallbackContext, 
        user_id: str
    ) -> None:
        """
        Handle what happens when user violates cooldown period.
        
        [PLACEHOLDER 24] - Cooldown Violation Response
        
        CUSTOMIZE THIS METHOD:
        - Define response to cooldown violations
        - Send custom error messages
        - Log security events
        - Implement escalating penalties
        
        RESPONSE OPTIONS:
        1. Send error message to user
        2. Log security event
        3. Increase cooldown period for repeat offenders
        4. Notify administrators
        5. Return helpful information about wait time
        """
        
        # [PLACEHOLDER 25] - Calculate Remaining Time
        remaining_time = self._get_remaining_cooldown_time(user_id)
        
        # [PLACEHOLDER 26] - Custom Error Response
        # Customize the message users see when in cooldown
        error_message = f"""
        Request rate limit exceeded. Please wait {remaining_time} seconds before trying again.
        
        [CUSTOMIZE THIS MESSAGE]
        - Add your app name
        - Include helpful information
        - Provide alternative actions
        - Add contact information
        """
        
        # [PLACEHOLDER 27] - Response Delivery Method
        # Choose how to deliver the error message
        # Options depend on your agent architecture:
        
        # Option 1: Set response in context
        # context.response = error_message
        
        # Option 2: Log for debugging
        print(f"Cooldown violation by user {user_id}: {remaining_time}s remaining")
        
        # Option 3: Send notification
        # self._notify_administrators(user_id, "cooldown_violation")
    
    def _get_remaining_cooldown_time(self, user_id: str) -> int:
        """
        Get remaining cooldown time for a user.
        
        [PLACEHOLDER 28] - Remaining Time Calculation
        
        CUSTOMIZE THIS METHOD:
        - Implement time calculation logic
        - Handle timezone considerations
        - Add custom time formatting
        """
        
        try:
            # [PLACEHOLDER 29] - API Call for Remaining Time
            if COOLDOWN_API_URL:
                response = requests.get(
                    f"{COOLDOWN_API_URL}/remaining/{user_id}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('remaining_seconds', 0)
            
            # [PLACEHOLDER 30] - Fallback Time Calculation
            # Implement local calculation if API unavailable
            return COOLDOWN_PERIOD_SECONDS
            
        except Exception as e:
            print(f"Error getting remaining time: {e}")
            return COOLDOWN_PERIOD_SECONDS
    
    # [PLACEHOLDER 31] - Additional Helper Methods
    # Add any other methods you need for your specific use case:
    
    def _notify_administrators(self, user_id: str, event_type: str) -> None:
        """
        Notify administrators of important events.
        
        [PLACEHOLDER 32] - Admin Notification Logic
        CUSTOMIZE: Add your notification system integration
        - Email notifications
        - Slack/Discord webhooks
        - Database logging
        - Monitoring system alerts
        """
        pass  # Implement your notification logic here
    
    def _get_user_cooldown_settings(self, user_id: str) -> dict:
        """
        Get user-specific cooldown settings.
        
        [PLACEHOLDER 33] - User-Specific Settings
        CUSTOMIZE: Implement different cooldown rules for different users
        - Premium users might have shorter cooldowns
        - New users might have longer cooldowns
        - Admins might bypass cooldowns entirely
        """
        return {
            'cooldown_seconds': COOLDOWN_PERIOD_SECONDS,
            'max_requests_per_hour': 100,  # Example additional limit
            'bypass_cooldown': False
        }
    
    def _log_cooldown_event(self, user_id: str, event_type: str, details: dict = None) -> None:
        """
        Log cooldown-related events for analytics and debugging.
        
        [PLACEHOLDER 34] - Event Logging
        CUSTOMIZE: Add your logging and analytics integration
        - Application logs
        - Analytics platforms
        - Monitoring systems
        - Audit trails
        """
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'user_id': user_id,
            'event_type': event_type,  # 'cooldown_start', 'cooldown_violation', etc.
            'details': details or {}
        }
        # Implement your logging logic here
        print(f"Cooldown event: {log_entry}")


# [PLACEHOLDER 35] - Plugin Registration
# Add code to register your plugin with the agent system
# This depends on your specific ADK setup:

def register_plugin(agent: BaseAgent) -> None:
    """
    Register the cooldown plugin with an agent.
    
    [PLACEHOLDER 36] - Registration Logic
    CUSTOMIZE: Implement how your plugin gets registered
    """
    plugin = CooldownPlugin()
    agent.add_plugin(plugin)  # Replace with actual registration method


# [PLACEHOLDER 37] - Configuration Validation
def validate_configuration() -> bool:
    """
    Validate that all required configuration is present.
    
    [PLACEHOLDER 38] - Validation Logic
    CUSTOMIZE: Add checks for your required configuration
    """
    if not COOLDOWN_API_URL:
        print("WARNING: COOLDOWN_API_URL not configured")
        return False
    
    if COOLDOWN_PERIOD_SECONDS <= 0:
        print("ERROR: COOLDOWN_PERIOD_SECONDS must be positive")
        return False
    
    return True


# ===== USAGE EXAMPLES =====
"""
EXAMPLE 1: Basic Setup
======================
1. Set COOLDOWN_PERIOD_SECONDS = 30  # 30 second cooldown
2. Set API_SERVER_URL environment variable to your backend
3. Replace _extract_user_id logic to get user ID from your system
4. Deploy and test

EXAMPLE 2: E-commerce Rate Limiting
===================================
# For an e-commerce site preventing rapid order attempts:
COOLDOWN_PERIOD_SECONDS = 120  # 2 minutes between orders
COOLDOWN_API_URL = "https://shop-api.com/rate-limit"

# In _extract_user_id:
return request.headers.get('customer-id') or request.session_id

# In _handle_cooldown_violation:
error_message = "Please wait 2 minutes between order attempts for security."

EXAMPLE 3: Gaming Application
=============================
# For a gaming app preventing spam actions:
COOLDOWN_PERIOD_SECONDS = 5  # 5 seconds between game actions
COOLDOWN_API_URL = "https://game-backend.com/cooldown"

# In _extract_user_id:
return context.player_id

# Add game-specific logic:
def _get_action_type(self, request):
    return request.metadata.get('game_action', 'unknown')

EXAMPLE 4: Content Moderation
=============================
# For content platforms preventing spam posting:
COOLDOWN_PERIOD_SECONDS = 300  # 5 minutes between posts
COOLDOWN_API_URL = "https://content-api.com/moderation/cooldown"

# In _handle_cooldown_violation:
error_message = "To prevent spam, please wait 5 minutes between posts."

# Add content-specific logging:
def _log_content_attempt(self, user_id, content_type):
    # Log attempted content creation for analysis

EXAMPLE 5: API Rate Limiting
============================
# For API services with usage quotas:
COOLDOWN_PERIOD_SECONDS = 60  # 1 minute between API calls
COOLDOWN_API_URL = "https://api-gateway.com/rate-limit"

# In _extract_user_id:
return request.headers.get('api-key') or request.client_ip

# Add quota tracking:
def _check_daily_quota(self, user_id):
    # Check if user has exceeded daily API quota
    pass

CUSTOMIZATION CHECKLIST:
========================
□ Replace COOLDOWN_PERIOD_SECONDS with your desired duration
□ Set COOLDOWN_API_URL to your backend endpoint
□ Implement _extract_user_id for your user identification system
□ Customize _handle_cooldown_violation for your error responses
□ Add any additional configuration variables you need
□ Implement proper error handling for your environment
□ Add logging and monitoring for your analytics system
□ Test with your specific agent and request types
□ Configure environment variables for deployment
□ Add any business-specific validation rules

DEPLOYMENT STEPS:
=================
1. Copy this template to your project
2. Fill in all [PLACEHOLDER] sections
3. Set environment variable API_SERVER_URL
4. Test locally with your agent
5. Deploy to your environment
6. Monitor cooldown effectiveness
7. Adjust timing and logic as needed
"""
