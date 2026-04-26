"""Property Location Strategy Agent - Root Agent Definition.

This module defines the root agent for the Location Strategy Pipeline.
It uses a SequentialAgent to orchestrate 6 specialized sub-agents:

1. MarketResearchAgent - Live web research with Google Search
2. LocationMappingAgent - Competitor mapping with Maps Places API
3. GapAnalysisAgent - Quantitative analysis with Python code execution
4. StrategyAdvisorAgent - Strategic synthesis with extended reasoning
5. ReportGeneratorAgent - HTML executive report generation
6. InfographicGeneratorAgent - Visual infographic generation

The pipeline analyzes a target location for a specific business type and
produces comprehensive location intelligence including recommendations,
an HTML report, and an infographic.

Authentication:
    Uses Google AI Studio (API key) instead of Vertex AI.
    Set environment variables:
        GOOGLE_API_KEY=your_api_key
        GOOGLE_GENAI_USE_VERTEXAI=FALSE
        MAPS_API_KEY=your_maps_api_key

Usage:
    Run with: adk web app (because i placed it in a /app folder and the agent is agent.py - it will look for this agent.py by default)

    The agent expects initial state variables:
    - target_location: The geographic area to analyze (e.g., "Melbourne, Australia")
    - property_type: Type of property to purchase/invest in (e.g., "standalone house, 4 bedroom house apartment, townhouse")
    
    Optional state variables:
    - maps_api_key: Google Maps API key for Places search
"""

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

from .config import APP_NAME, FAST_MODEL
from .sub_agents.competitor_mapping.agent import location_mapping_agent
from .sub_agents.gap_analysis.agent import gap_analysis_agent
from .sub_agents.infographic_generator.agent import infographic_generator_agent
from .sub_agents.intake_agent.agent import intake_agent
from .sub_agents.market_research.agent import market_research_agent
from .sub_agents.report_generator.agent import report_generator_agent
from .sub_agents.strategy_advisor.agent import strategy_advisor_agent

# location_strategy_pipeline
location_strategy_pipeline = SequentialAgent(
    name="LocationStrategyPipeline",
    description="""Comprehensive retail location strategy analysis pipeline.

This agent analyzes a target location for a specific property type and produces:
1. Market research findings from live web data
2. Location mapping from Google Maps Places API
3. Quantitative gap analysis with zone rankings
4. Strategic recommendations with structured JSON output
5. Professional HTML executive report
6. Visual infographic summary

To use, get the following details:
- target_location: {target_location}
- property_type: {property_type}

The analysis runs automatically through all stages and produces artifacts
including JSON report, HTML report, and infographic image.
""",
    sub_agents=[
        market_research_agent,  # Part 1: Market research with search
        location_mapping_agent,  # Part 2A: Location mapping with Maps
        gap_analysis_agent,  # Part 2B: Gap analysis with code exec
        strategy_advisor_agent,  # Part 3: Strategy synthesis
        report_generator_agent,  # Part 4: HTML report generation
        infographic_generator_agent,  # Part 5: Infographic generation
    ],
)

# Root agent orchestrating the complete location strategy pipeline
root_agent = Agent(
    model=FAST_MODEL,
    name=APP_NAME,
    description="A strategic partner for a house property for ownership or investment purposes, guiding them to optimal physical locations that foster growth and profitability.",
    instruction="""Your primary role is to orchestrate the property location analysis.
1. Start by greeting the user.
2. Check if the `TARGET_LOCATION` (Geographic area to analyze (e.g., "St Ablbans, Melbourne")) and `PROPERTY_TYPE` (Type of property (e.g., "new house", "apartment", "townhouse")) have been provided.
3. If they are missing, **ask the user clarifying questions to get the required information.**
4. Once you have the necessary details, call the `IntakeAgent` tool to process them.
5. After the `IntakeAgent` is successful, delegate the full analysis to the `LocationStrategyPipeline`.
Your main function is to manage this workflow conversationally.""",
    sub_agents=[location_strategy_pipeline],
    tools=[AgentTool(intake_agent)],  # Part 0: Parse user request
)

from google.adk.apps import App

app = App(root_agent=root_agent, name="app")
