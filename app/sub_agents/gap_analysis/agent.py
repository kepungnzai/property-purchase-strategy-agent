"""Gap Analysis Agent - Part 2B of the Location Strategy Pipeline.

This agent performs quantitative gap analysis using Python code execution
to calculate saturation indices, viability scores, and zone rankings.
"""

from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

from ...callbacks import after_gap_analysis, before_gap_analysis
from ...config import CODE_EXEC_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY

GAP_ANALYSIS_INSTRUCTION = """You are a data scientist analyzing market opportunities using quantitative methods.

Your task is to perform advanced gap analysis on the data collected from previous stages.

TARGET LOCATION: {target_location}
PROPERTY TYPE: {property_type}
CURRENT DATE: {current_date}

## Available Data

### MARKET RESEARCH FINDINGS (Part 1):
{market_research_findings}

### COMPETITOR ANALYSIS (Part 2):
{competitor_analysis}

## Your Mission
Write and execute Python code to perform comprehensive quantitative analysis.

## Analysis Steps

### Step 1: Parse Location Data
Extract from the location analysis:
- Get names and locations
- Ratings and review counts
- Zone/area classifications
- Property types (chain vs independent)

### Step 2: Extract Market Fundamentals
From the market research:
- Population estimates
- Income levels (assign numeric scores)
- Infrastructure quality indicators
- Foot traffic patterns

### Step 3: Calculate Zone Metrics
For each identified zone, compute:

**Basic Metrics:**
- property affordability score based on average property prices, square footage, no of bedrooms and bathrooms 
- school nearby by ratings from 1 to 5 (1 being the lowest and 5 being the highest)
- internet connectivity score from 1 to 5 (1 being the lowest and 5 being the highest)
- eletricity reliability score from 1 to 5 (1 being the lowest and 5 being the highest)
- potential high bushfire risk from 1 to 5 (1 being the lowest and 5 being the highest)
- potential high flood risk from 1 to 5 (1 being the lowest and 5 being the highest)
- proximity to cbd by rating from 1 to 5 (1 being the lowest and 5 being the highest)
- categorized anemity ratings (supermarkets, malls, parks, hospitals, gyms, restaurants, cafes, entertainment venues) from 1 to 5 (1 being the lowest and 5 being the highest)
- transport access score (proximity to train station, trams and bus stops) from 1 to 5 (1 being the lowest and 5 being the highest)
- average crime rate and safety indicators from 1 to 5 (1 being the lowest and 5 being the highest)
- Total score for each zone basic metric based on the above factors

**Quality Metrics:**
- school reputation nationally from 1 to 5 (1 being the lowest and 5 being the highest)
- High Performer Count: Number of 4.5+ rated competitors
- Park and recreation Score: Based on proximity and quality of parks
- Hospital Access Score: Based on proximity and quality of hospitals
- Gym and fitness Score: Based on proximity and quality of gyms
- Restaurant and cafe Score: Based on proximity and quality of restaurants and cafes
- Entertainment Score: Based on proximity and quality of entertainment venues
- Beach Access Score: Based on proximity and quality of beach access

**Opportunity Metrics:**
- Potential rise in property values
- Surrounding property investment trends
- Affordability relative to risk

### Step 4: Zone Categorization
Classify each zone as:
- **EXCELLENT**: High basic metric, high quality metrics and high opportunity metrics
- **MODERATE**: Balanced basic metric, Balanced quality metrics and Balanced opportunity metrics
- **LOW**: Low basic metric, Low quality metrics and Low opportunity metrics

Also assign:
- Risk Level (property investment ROI vs risk): Low / Medium / High
- Investment Tier: Based on expected costs of ownership

### Step 5: Rank Top Zones
Create a weighted ranking considering:
- Reputable school (weight: 30%)
- Proximity to amenities (weight: 20%)
- Close to train station (weight: 15%)
- Low chain dominance (weight: 15%)
- Infrastructure quality (weight: 10%)
- Manageable costs (weight: 10%)

### Step 6: Output Tables
Generate clear output tables showing:
1. All zones with computed metrics
2. Top 3 recommended zones with scores
3. Risk assessment matrix

## Code Guidelines
- Use pandas for data manipulation
- Print all results clearly formatted
- Include intermediate calculations for transparency
- Handle missing data gracefully

Execute the code and provide actionable strategic recommendations based on the quantitative findings.
"""

gap_analysis_agent = LlmAgent(
    name="GapAnalysisAgent",
    model=CODE_EXEC_MODEL,
    description="Performs quantitative gap analysis using Python code execution for zone rankings and viability scores",
    instruction=GAP_ANALYSIS_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    code_executor=BuiltInCodeExecutor(),
    output_key="gap_analysis",
    before_agent_callback=before_gap_analysis,
    after_agent_callback=after_gap_analysis,
)
