# Travel Itinerary Crew

A hierarchical CrewAI setup: a Manager agent delegates to a Researcher,
Local Expert, and Logistics Planner, then a Writer agent turns all of it
into a final day-by-day itinerary.

## Setup

```bash
cd travel_crew
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:
- `ANTHROPIC_API_KEY` — required, powers every agent
- `SERPER_API_KEY` — optional, gives agents real web search (free tier at serper.dev). Without it, agents reason from the model's own knowledge only — fine for a first test, not for anything current (prices, hours, current openings).

## Run

```bash
python main.py
```

It defaults to a test run for your London–Barcelona–Amalfi trip. To
change the trip, edit the `inputs` dict at the bottom of `main.py`:

```python
inputs = {
    "destinations": "Tokyo, Kyoto",
    "dates": "7 days in April",
    "trip_style": "food-focused, mid-range, some hiking",
}
```

## How the hierarchy works

Unlike a fixed sequential pipeline, the **Manager agent** decides at
runtime how to route work between the Researcher, Local Expert, and
Logistics Planner — it can re-delegate or ask for revisions if an
output isn't good enough before handing off to the Writer. This is
slower and more token-hungry than sequential, but closer to genuine
multi-agent coordination.

## What's deliberately left out of v1

- No booking/live-price integration (flights, hotels)
- No pull from your actual travel-planning-standards — trip style is
  passed in per-run as a plain string for now
- No persistence — each run is a fresh itinerary, nothing is saved

## Natural next steps

1. Swap `SerperDevTool` for Google Places API to reuse your existing
   First Sip key and get richer local data
2. Feed your travel-planning-standards doc into `trip_style` or as a
   system-level addition to the Writer agent's backstory
3. Add a simple output step that saves the itinerary to a markdown
   file per trip
