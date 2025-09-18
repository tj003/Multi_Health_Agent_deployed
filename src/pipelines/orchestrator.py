from __future__ import annotations
import asyncio
import logging
from typing import List, Dict
from crewai import Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import GROQ_API_KEY, LLM_MODEL, MAX_ITEMS, RSS_FEEDS
from src.telemetry.metrics import timed
from src.tools.news_tool import fetch_feeds
from src.agents.data_miner_agent import DataMinerAgent
from src.agents.summarizer_agent import MedicalSummarizerAgent
from src.agents.decision_agent import DecisionMakerAgent

logger = logging.getLogger(__name__)

# Shared LLMs 
llm = ChatGroq(model=LLM_MODEL, groq_api_key=GROQ_API_KEY, temperature=0.2, max_tokens=256)
clf_llm = ChatGroq(model=LLM_MODEL, groq_api_key=GROQ_API_KEY, temperature=0.0, max_tokens=32)

# Load prompts
SUMMARIZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", open("src/prompts/summarizer_prompt.txt", "r", encoding="utf-8").read()),
    ("user", "Title: {title}\nLink: {link}\nPublished: {published}")
])

CLASSIFIER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", open("src/prompts/classifier_prompt.txt", "r", encoding="utf-8").read()),
    ("user", "Summary: {summary}")
])


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
async def summarize_one(item: Dict) -> Dict:
    chain = SUMMARIZER_PROMPT | llm
    with timed("summarize_one"):
        try:
            out = await chain.ainvoke(item)
            return {**item, "summary": out.content.strip()}
        except Exception as e:
            logger.error(f" Summarization failed for {item.get('title')}: {e}")
            return {**item, "summary": "N/A"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
async def classify_one(item: Dict) -> Dict:
    chain = CLASSIFIER_PROMPT | clf_llm
    with timed("classify_one"):
        try:
            out = await chain.ainvoke({"summary": item["summary"]})
            label = out.content.strip()
        except Exception as e:
            logger.error(f" Classification failed for {item.get('title')}: {e}")
            label = "Informative" 
    if label not in ("Actionable Advice", "Informative"):
        # Fallback 
        text_lower = item["summary"].lower()
        keywords = [
            "should", "must", "recommend", "avoid", "practice", "take", "limit",
            "increase", "reduce", "exercise", "monitor", "check", "consult",
            "vaccinate", "follow", "tips", "guidelines", "advice", "steps",
            "ways", "strategies", "methods", "how to", "risk", "prevention",
            "healthy", "improve", "protect", "manage", "treatment"
        ]
        label = "Actionable Advice" if any(k in text_lower for k in keywords) else "Informative"

    return {**item, "category": label}


# --- Async Orchestration ---
async def run_pipeline(max_items: int = MAX_ITEMS) -> List[Dict]:
    # Step 1: Fetch feeds concurrently
    with timed("fetch_feeds"):
        items = await fetch_feeds(RSS_FEEDS, max_items=max_items)

    seen, deduped = set(), []
    for it in items:
        key = (it.get("title", ""), it.get("link", ""))
        if key not in seen:
            seen.add(key)
            deduped.append(it)

    logger.info(f" Retrieved {len(deduped)} unique articles")

    # Step 2: Summarize concurrently
    with timed("summarize_batch"):
        summarized = await asyncio.gather(*[summarize_one(it) for it in deduped])

    # --- Step 3. Classify concurrently ---
    with timed("classify_batch"):
        classified = await asyncio.gather(*[classify_one(it) for it in summarized])

    #  Log agentic style outputs
    for art in classified:
        logger.info(f" Decision Maker | {art['title']} → {art['category']}")

    return classified


# --- Crew Setup ---
async def kickoff_crew() -> List[Dict]:
    """CrewAI Orchestration with async tasks."""
    async def fetch_action():
        return await fetch_feeds(RSS_FEEDS, max_items=MAX_ITEMS)

    async def summarize_action(items):
        return await asyncio.gather(*[summarize_one(it) for it in items])

    async def classify_action(items):
        return await asyncio.gather(*[classify_one(it) for it in items])

    fetch_task = Task(
        description="Fetch latest health news",
        agent=DataMinerAgent,
        async_fn=fetch_action,
        expected_output="List of news dicts {title, link, published, source}"
    )

    summarize_task = Task(
        description="Summarize each news item",
        agent=MedicalSummarizerAgent,
        async_fn=summarize_action,
        expected_output="News items augmented with 'summary'"
    )

    classify_task = Task(
        description="Classify summaries as Actionable Advice or Informative",
        agent=DecisionMakerAgent,
        async_fn=classify_action,
        expected_output="News items augmented with 'category'"
    )

    crew = Crew(
        agents=[DataMinerAgent, MedicalSummarizerAgent, DecisionMakerAgent],
        tasks=[fetch_task, summarize_task, classify_task],
        process=Process.sequential,  # can switch to parallel if independent
        verbose=True,
    )

    results = await crew.kickoff_async()
    return results
