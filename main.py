"""
Travel Itinerary Crew — hierarchical multi-agent trip planner.

A manager agent delegates work to three specialist agents, then a
Writer agent synthesizes everything into a final itinerary.

Run:
    python main.py
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

# ---------------------------------------------------------------------------
# LLM config — all agents run on Claude via the Anthropic API
# ---------------------------------------------------------------------------
llm = LLM(
    model="anthropic/claude-sonnet-4-5-20250929",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Web search tool (optional — only works if SERPER_API_KEY is set).
# If you skip this, the agents will rely on the LLM's own knowledge,
# which is fine for a first test run but won't have current info.
search_tool = SerperDevTool() if os.getenv("SERPER_API_KEY") else None
tools = [search_tool] if search_tool else []

# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------
researcher = Agent(
    role="Destination Researcher",
    goal="Identify the best neighborhoods, seasonal considerations, and "
         "overall shape of the trip for {destinations} during {dates}",
    backstory="A well-traveled researcher who quickly builds a solid "
              "overview of any destination before anyone visits it.",
    tools=tools,
    llm=llm,
    verbose=True,
)

local_expert = Agent(
    role="Local Expert",
    goal="Surface specific restaurants, activities, and experiences in "
         "{destinations} that fit the trip's style: {trip_style}",
    backstory="Someone who has lived in or extensively explored these "
              "destinations and knows what's actually worth doing, not "
              "just what's popular.",
    tools=tools,
    llm=llm,
    verbose=True,
)

logistics_planner = Agent(
    role="Logistics Planner",
    goal="Sequence the trip across {dates}, accounting for travel time "
         "between locations, opening hours, and realistic pacing",
    backstory="A meticulous planner who has seen too many itineraries "
              "fall apart from unrealistic scheduling.",
    tools=tools,
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Itinerary Writer",
    goal="Turn all research and logistics into a clear, day-by-day "
         "itinerary for {destinations}",
    backstory="A travel writer who turns raw research into an itinerary "
              "someone could actually follow.",
    llm=llm,
    verbose=True,
)

# The manager agent — only used to delegate/coordinate, has no tasks of
# its own. This is what makes the process "hierarchical" rather than a
# fixed sequential pipeline.
manager = Agent(
    role="Trip Planning Manager",
    goal="Coordinate the Researcher, Local Expert, and Logistics Planner "
         "to produce everything the Itinerary Writer needs for "
         "{destinations} during {dates}",
    backstory="An experienced project lead who knows how to get the "
              "right specialist working on the right piece at the "
              "right time.",
    llm=llm,
    allow_delegation=True,
    verbose=True,
)

# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
research_task = Task(
    description="Research {destinations} for a trip during {dates}. "
                "Cover neighborhoods worth basing in, seasonal notes, "
                "and general trip shape.",
    expected_output="A structured overview covering each destination's "
                     "best neighborhoods and any seasonal considerations.",
    agent=researcher,
)

local_picks_task = Task(
    description="Using the destination research, identify specific "
                "restaurants, activities, and experiences that match "
                "this trip style: {trip_style}.",
    expected_output="A list of specific, named recommendations per "
                     "destination, each with a one-line reason it fits "
                     "the trip style.",
    agent=local_expert,
    context=[research_task],
)

logistics_task = Task(
    description="Sequence the trip across {dates}. Account for travel "
                "time between destinations/neighborhoods, opening "
                "hours, and realistic daily pacing.",
    expected_output="A day-by-day skeleton (Day 1, Day 2, ...) showing "
                     "which destination/neighborhood each day covers "
                     "and rough time blocks.",
    agent=logistics_planner,
    context=[research_task, local_picks_task],
)

writing_task = Task(
    description="Combine the research, local recommendations, and "
                "logistics into one polished day-by-day itinerary for "
                "{destinations}.",
    expected_output="A complete markdown itinerary: one section per "
                     "day, with named stops, rough timing, and a short "
                     "note on why each stop was chosen.",
    agent=writer,
    context=[research_task, local_picks_task, logistics_task],
)

# ---------------------------------------------------------------------------
# Crew — hierarchical process
# ---------------------------------------------------------------------------
crew = Crew(
    agents=[researcher, local_expert, logistics_planner, writer],
    tasks=[research_task, local_picks_task, logistics_task, writing_task],
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True,
)

if __name__ == "__main__":
    inputs = {
        "destinations": "London, Barcelona, Amalfi Coast",
        "dates": "10 days in late September",
        "trip_style": "high-end, experiential couple travel — "
                       "good food, some culture, not overpacked",
    }
    result = crew.kickoff(inputs=inputs)
    print("\n\n=== FINAL ITINERARY ===\n")
    print(result)
