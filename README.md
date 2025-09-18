# Multi-Agent Health News System (CrewAI)

##  Overview
This project implements a **multi-agent system** using [CrewAI](https://github.com/joaomdmoura/crewAI).  
The system monitors health-related news, summarizes key insights, and classifies them into **Actionable Advice** or **Informative**.

It is designed as part of an **AI Engineer assessment for GOQii**.

---

## System Goals
- Automate health news monitoring.
- Provide concise medical summaries.
- Flag actionable health alerts for quick response.

---

##  Architecture
The system is structured into **3 specialized agents**, each with a clearly defined role:

1. **Data Miner Agent**
   - Fetches latest health news via RSS feeds (e.g., CDC, NHS, MedicalXpress).
   - Outputs structured news items (title, link, published date).

2. **Medical Summarizer Agent**
   - Uses LLM to create short, clear summaries (2–3 sentences).
   - Extracts actionable insights if present.

3. **Decision Maker Agent**
   - Classifies summaries into:
     - **Actionable Advice** (e.g., recalls, prevention tips, vaccination alerts).
     - **Informative** (e.g., general research findings, correlations).
   - Falls back to rule-based classification if LLM fails.

---

##  Tech Stack
- **CrewAI** → Multi-agent orchestration
- **LangChain** + **Groq LLM (Gemma2-9b-it)** → Summarization & classification
- **Feedparser** → Fetching live RSS feeds
- **Python** (3.10+)
- **dotenv** → Environment variable handling

---

##  How It Works
1. **Data Miner** collects the latest 5 health news articles.
2. **Summarizer** generates concise summaries.
3. **Decision Maker** classifies each summary.
4. **Orchestrator** connects these agents in sequence.


Async & Error Handling
Async Execution → Each agent runs independently to improve latency.

Error Handling →

If LLM fails → fallback to rule-based keywords.

If feeds fail → gracefully log & continue with available sources.

 Performance & Cost Insights
Latency:

Data mining: <1s per feed

Summarization: ~1.2s per article (Groq API, Gemma2-9b-it)

Classification: ~0.8s per summary

Scaling:

System can be extended to multiple feeds, languages, or domains.

Cost:

Using Groq inference is cheaper than GPT-4, while keeping good quality.

Rule-based fallback ensures cost saving when LLM calls fail.


▶️ Usage
1. Clone Repo

git clone https://github.com/<your-username>/Multi_Health_Agent.git
cd Multi_Health_Agent


2. Setup Environment

python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Add .env

GROQ_API_KEY=your_api_key_here
 [ 
 
#### How to obtain a free GROQ API Key:
1. Go to [https://groq.com/](https://groq.com/) and log in.  
2. Click **Start Building**.  
3. Navigate to **API Keys** → **Create API Key**.  
4. Copy the key and paste it in your `.env` file.  

]