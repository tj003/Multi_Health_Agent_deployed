# 🧠 Multi-Agent Health News System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Hugging Face Spaces](https://img.shields.io/badge/🤗-HuggingFace%20Space-orange)](https://huggingface.co/spaces/your-username/multi-health-agent)

## 📌 Overview
This project implements a **multi-agent system** using [CrewAI](https://github.com/joaomdmoura/crewAI).  
It monitors health-related news, summarizes key insights, and classifies them into **Actionable Advice** or **Informative**.

🩺 Built as part of an **AI Engineer assessment for GOQii**.

---

## ⚙️ System Architecture
There are **3 specialized agents**, each with a clearly defined role:

### 1. Data Miner Agent
- Fetches latest health news from RSS feeds (e.g., CDC, NHS, MedicalXpress).
- Outputs structured news items (title, link, published date).

### 2. Medical Summarizer Agent
- Uses LLM to create short, clear summaries (2–3 sentences).
- Extracts actionable insights if present.

### 3. Decision Maker Agent
- Classifies summaries into:
  - **Actionable Advice** (e.g., recalls, vaccination alerts, prevention tips)
  - **Informative** (e.g., general research findings)
- Falls back to rule-based classification if LLM fails.

---

## 🛠️ Tech Stack
- **CrewAI** → Multi-agent orchestration
- **LangChain** + **Groq LLM (Gemma2-9b-it)**
- **Feedparser** → Fetching live RSS feeds
- **Python** (3.10+)
- **dotenv** → Environment variables

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/multi-health-agent.git
cd multi-health-agent
pip install -r requirements.txt
python main.py
