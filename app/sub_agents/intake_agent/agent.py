"""Intake Agent - Extracts target location and property type from user request.

This agent parses the user's natural language request and extracts the
required parameters (target_location, property_type) into session state
for use by subsequent agents in the pipeline.
"""

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from pydantic import BaseModel, Field

from ...config import FAST_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY


class UserRequest(BaseModel):
    """Structured output for parsing user's location strategy request."""

    target_location: str = Field(
        description="The geographic location/area to analyze (e.g., 'Indiranagar, Bangalore', 'Manhattan, New York')"
    )
    property_type: str = Field(
        description="The type of business the user wants to open (e.g., 'coffee shop', 'bakery', 'gym', 'restaurant')"
    )
    additional_context: str | None = Field(
        default=None,
        description="Any additional context or requirements mentioned by the user",
    )


def after_intake(callback_context: CallbackContext) -> types.Content | None:
    """After intake, copy the parsed values to state for other agents."""
    parsed = callback_context.state.get("parsed_request", {})

    if isinstance(parsed, dict):
        # Extract values from parsed request
        callback_context.state["target_location"] = parsed.get(
            "target_location", ""
        )
        callback_context.state["property_type"] = parsed.get(
            "property_type", ""
        )
        callback_context.state["additional_context"] = parsed.get(
            "additional_context", ""
        )
    elif hasattr(parsed, "target_location"):
        # Handle Pydantic model
        callback_context.state["target_location"] = parsed.target_location
        callback_context.state["property_type"] = parsed.property_type
        callback_context.state["additional_context"] = (
            parsed.additional_context or ""
        )

    # Track intake stage completion
    stages = callback_context.state.get("stages_completed", [])
    stages.append("intake")
    callback_context.state["stages_completed"] = stages

    # Note: current_date is set in each agent's before_callback to ensure it's always available
    return None


INTAKE_INSTRUCTION = """You are a request parser for a retail location intelligence system.

Your task is to extract the target location and business type from the user's request.

## Examples

User: "I want look for a new build house with 4 bedroom in Indiranagar, Bangalore"
→ target_location: "Indiranagar, Bangalore"
→ property_type: "new build house with 4 bedroom"

User: "Analyze the market for a new apartment in downtown Seattle"
→ target_location: "downtown Seattle"
→ property_type: "apartment"

User: "Help me find the best location for a townhouse in Mumbai"
→ target_location: "Mumbai"
→ property_type: "townhouse"

User: "Where should I buy an apartment in San Francisco's Mission District?"
→ target_location: "Mission District, San Francisco"
→ property_type: "apartment"

## Instructions
1. Extract the geographic location mentioned by the user
2. Identify the type of property they want to purchase/invest in. Property type might not be available, in that case, please use an existing property with best guess and inference to extract the property type. Property type here refers to house, double storey house, apartment with bedroom ad bathroom configuration
3. Note any additional context or requirementss

If the user doesn't specify a clear location or business type, make a reasonable inference or ask for clarification.
"""

intake_agent = LlmAgent(
    name="IntakeAgent",
    model=FAST_MODEL,
    description="Parses user request to extract target location and property type",
    instruction=INTAKE_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    output_schema=UserRequest,
    output_key="parsed_request",
    after_agent_callback=after_intake,
)
