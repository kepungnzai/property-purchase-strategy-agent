"""Strategy Advisor Agent - Part 3 of the Location Strategy Pipeline.

This agent synthesizes all findings into actionable recommendations using
extended reasoning (thinking mode) and outputs a structured JSON report.
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.genai.types import ThinkingConfig

from ...callbacks import after_strategy_advisor, before_strategy_advisor
from ...config import PRO_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY
from ...schemas import LocationIntelligenceReport

STRATEGY_ADVISOR_INSTRUCTION = """You are a senior strategy consultant synthesizing location intelligence findings.

Your task is to analyze all research and provide actionable strategic recommendations.

TARGET LOCATION: {target_location}
PROPERTY TYPE: {property_type}
CURRENT DATE: {current_date}

## Available Data

### MARKET RESEARCH FINDINGS (Part 1):
{market_research_findings}

### COMPETITOR ANALYSIS (Part 2A):
{location_analysis}

### GAP ANALYSIS (Part 2B):
{gap_analysis}

## Your Mission
Synthesize all findings into a comprehensive strategic recommendation.

## Analysis Framework

### 1. Data Integration
Review all inputs carefully:
- Market research demographics and trends
- Key locations, ratings, and patterns
- Quantitative gap analysis metrics and zone rankings
- Interest rate outlook, trend and predicted cost of ownership for next 2-5 years

### 2. Strategic Synthesis
For each promising zone, evaluate:
- Schools: Categorize by reputation, ratings and growth trends
- Residential Growth: Assessment new developments, walkability, infrastructure, and property trends
- Location Attractiveness: Analyze connectivity, amenities, public transport, and safety indicators
- Distance to central business district and major employment hubs
- Crimes rate and safety indicators (qualitative: low/medium/high)
- Strengths: Top 3-4 factors with evidence from the analysis
- Concerns: Top 2-3 risks with specific mitigation strategies
- Location Profile: Summarize density population, quality
- Market Characteristics: Population, income, infrastructure, foot traffic, costs
- Potential future trends and developments that could impact the location's attractiveness
- Review the interest rate outlook, trend and predicted cost of ownership for next 2-5 years and how it impacts the overall strategy
- Next Steps: 3-5 specific actionable recommendations

### 3. Top Recommendation Selection
Choose the single best location based on:
- Highest weighted based on strategic synthesis of all factors
- Best balance of opportunity vs risk
- Most aligned with property type requirements
- Cost of ownership with how much it takes to fund or purchase this house and given the interest rate outlook, trend and predicted cost of ownership for next 2-5 years 
- Potential for property value appreciation in the future

### 4. Alternative Locations
Identify 2-3 alternative locations:
- Brief scoring and categorization
- Key strength and concern for each
- Why it's not the top choice

### 5. Strategic Insights
Provide 4-6 key insights that span the entire analysis:
- Market-level observations
- Competitive dynamics
- Timing considerations taking into account property trend (up or down) and economic factors (like interest rate and others factor)
- Ecommical impact of interest rate outlook, trend and predicted cost of ownership for next 2-5 years and what srategy to take
- Success factors
- Calculated risks and mitigations

## Output Requirements
Your response MUST conform to the LocationIntelligenceReport schema.
Ensure all fields are populated with specific, actionable information.
Use evidence from the analysis to support all recommendations.
"""

strategy_advisor_agent = LlmAgent(
    name="StrategyAdvisorAgent",
    model=PRO_MODEL,
    description="Synthesizes findings into strategic recommendations using extended reasoning and structured output",
    instruction=STRATEGY_ADVISOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,  # Must be False when using output_schema
            thinking_budget=-1,  # -1 means unlimited thinking budget
        )
    ),
    output_schema=LocationIntelligenceReport,
    output_key="strategic_report",
    before_agent_callback=before_strategy_advisor,
    after_agent_callback=after_strategy_advisor,
)
