"""Competitor Mapping Agent - Part 2A of the Location Strategy Pipeline.

This agent maps competitors using the Google Maps Places API to get
ground-truth data about existing locations in the target area.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...callbacks import after_competitor_mapping, before_competitor_mapping
from ...config import FAST_MODEL, RETRY_ATTEMPTS, RETRY_INITIAL_DELAY
from ...tools import search_places

COMPETITOR_MAPPING_INSTRUCTION = """You are a market intelligence analyst specializing in competitive landscape analysis.

Your task is to find, map and analyze schools, supermarket, shopping mall, amenities, train stations, tram, bus, highway access, road access park, university, parks, shopping mall and other business in the same area near in the target area using real Google Maps data. Take note how long it takes to central business centers or CBDs

TARGET LOCATION: {target_location}
CURRENT DATE: {current_date}

## Your Mission
Use the search_places function to get REAL data from Google Maps about existing competitors.

## Step 1: Search for Competitors
Call the search_places function with queries like:
- "Find schools, supermarket, shopping mall, amenities, train stations, tram, bus, highway access, road access park, university, parks, shopping mall and other business in the same area near {target_location}. Take note how long it takes to central business centers or CBDs (this can be a good selling point)"

## Step 2: Analyze the Results
For each location found, note:
- Location name
- Location Type
- Location/address
- Rating (out of 5)
- Number of reviews
- Business status (operational, etc.)

## Step 3: Identify Patterns
Analyze the competitive landscape:

### Geographic Clustering
- Are these locations clustered in specific areas/zones?
- Which areas have high concentration vs sparse presence?
- Are there any "dead zones" with no competitors?

### Location Types
- Shopping malls and retail areas
- Main roads and commercial corridors
- Residential neighborhoods
- Near transit (metro stations, bus stops)

### Quality Segmentation
- Premium tier: High-rated (4.5+), likely higher prices
- Mid-market: Ratings 4.0-4.4
- Budget tier: Lower ratings or basic offerings

## Step 4: Strategic Assessment
Provide insights on:
- Are there underserved areas with high demand potential?
- Potential for opening of new good schools, supermarket, shopping mall, amenities, train stations, tram, bus, highway access, road access park, university, parks, shopping mall and other business in the same area near the target location?
- Is the surrounding area within short distance away from the property location 
- Is the property located in an area with high flood risk?
- Is the property located in an area with high fire risk?
- Is there area geographically flat or sloped?

## Output Format
Provide a detailed location map with:
1. List of all locations found with their details
2. Zone-by-zone breakdown of location by proximity to the target location
3. Pattern analysis and clustering insights
4. Strategic opportunities and hazard warnings

Be specific and reference the actual data you receive from the search_places tool.
"""

competitor_mapping_agent = LlmAgent(
    name="CompetitorMappingAgent",
    model=FAST_MODEL,
    description="Maps competitors using Google Maps Places API for ground-truth competitor data",
    instruction=COMPETITOR_MAPPING_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[search_places],
    output_key="competitor_analysis",
    before_agent_callback=before_competitor_mapping,
    after_agent_callback=after_competitor_mapping,
)
