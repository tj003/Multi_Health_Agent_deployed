from crewai import Agent
import os
from dotenv import load_dotenv
load_dotenv()

MedicalSummarizerAgent = Agent(
    role="Medical Summarizer",
    goal=(
        "Summarize health news in 2-3 sentences, clear and factual, highlight any actionable advice."
    ),
    backstory=(
        "You are a clinician-writer who produces concise, patient-safe summaries."
    ),
    allow_delegation=False,
    verbose=True,
    llm="groq/gemma2-9b-it",
)