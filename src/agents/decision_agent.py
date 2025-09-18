from crewai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

DecisionMakerAgent = Agent(
    role="Decision Maker",
    goal=(
        "Classify each health news summary strictly as 'Actionable Advice' or 'Informative'.\n\n"
        "Return ONLY valid JSON in this format:\n"
        "{ \"category\": \"Actionable Advice\" }\n"
        "OR\n"
        "{ \"category\": \"Informative\" }\n\n"
        "Definitions:\n"
        "- Actionable Advice: Explicit steps, guidance, or warnings for people to act on.\n"
        "- Informative: Reports facts, studies, or general updates without instructions.\n\n"
        "Examples:\n"
        "Input: 'CDC recommends everyone get a flu shot this fall.'\n"
        "Output: { \"category\": \"Actionable Advice\" }\n\n"
        "Input: 'New study links sleep deprivation to heart disease.'\n"
        "Output: { \"category\": \"Informative\" }\n"
    ),
    backstory="You are a health policy reviewer who flags actionable public guidance vs general awareness.",
    allow_delegation=False,
    verbose=True,
    llm="groq/gemma2-9b-it"
)
