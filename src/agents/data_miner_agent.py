from crewai import Agent
import os
from dotenv import load_dotenv
load_dotenv()
DataMinerAgent = Agent(
    role="Data Miner",
    goal=(
        "Retrieve the latest health news items from trusted RSS sources with high recall, "
        "deduplicate by title/link, and provide clean JSON."
    ),
    backstory=(
        "You are a reliable web intelligence specialist focused on timely health news. "
        "You verify sources and return structured entries."
    ),
    allow_delegation=False,
    verbose=True,
    llm="groq/gemma2-9b-it"
)