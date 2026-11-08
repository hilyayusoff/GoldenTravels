# GoldenTravels: Multi-Agent Trip Planner

A personal project (September 2026) for planning trips with a team of AI agents. Built with CrewAI and Claude to explore hierarchical multi-agent orchestration, where a manager agent decides who does what instead of following a fixed pipeline.

## How it works

| Agent | Role |
| --- | --- |
| Trip Planning Manager | Coordinates the specialists, and re-delegates or asks for revisions when an output falls short |
| Destination Researcher | Neighbourhoods to base in, seasonal considerations and the overall shape of the trip |
| Local Expert | Specific restaurants, activities and experiences that match the trip style |
| Logistics Planner | Day-by-day sequencing with travel times, opening hours and realistic pacing |
| Itinerary Writer | Combines everything into the final day-by-day itinerary |

**Input:** destinations, dates and a trip style.
**Output:** a markdown itinerary with named stops, rough timings and a short reason for each choice.

A hierarchical process is slower and uses more tokens than a sequential one, but it lets the manager catch weak outputs before they reach the final itinerary.

## Stack

- Python and CrewAI (hierarchical process)
- Claude via the Anthropic API, powering every agent
- Serper web search (optional) for up-to-date information

## Running it

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # ANTHROPIC_API_KEY, plus SERPER_API_KEY for live search
python main.py
```

Trip details live in the `inputs` dict at the bottom of `main.py`, for example:

```python
inputs = {
    "destinations": "Tokyo, Kyoto",
    "dates": "7 days in April",
    "trip_style": "food-focused, mid-range, some hiking",
}
```

Without a Serper key, the agents rely on the model's own knowledge, so prices, opening hours and new openings may be out of date.

## Current scope

- No booking or live pricing for flights and hotels
- Trip style is passed in as plain text for each run
- Itineraries print to the console and aren't saved

## Ideas for later

- Google Places API for richer local data
- A saved set of personal travel preferences for the Writer agent
- Saving each itinerary to its own markdown file
