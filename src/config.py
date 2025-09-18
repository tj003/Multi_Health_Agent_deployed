from dotenv import load_dotenv
import os

load_dotenv()

# API Keys & LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma2-9b-it")  # 👈 lowercase safe default

# Pipeline configs
MAX_ITEMS = int(os.getenv("MAX_ITEMS", 8))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", 12))

# RSS Feeds
RSS_FEEDS = [u.strip() for u in os.getenv("RSS_FEEDS", "").split(",") if u.strip()]

if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment.")

# Provide defaults if not set in .env
if not RSS_FEEDS:
    RSS_FEEDS = [
        "https://www.sciencedaily.com/rss/health_medicine.xml",
        "https://www.medicalnewstoday.com/rss/health-news",  
        "https://rss.cnn.com/rss/cnn_health.rss",            
        "https://feeds.npr.org/1128/rss.xml",                
        "https://news.google.com/rss/search?q=who+health"    
    ]
