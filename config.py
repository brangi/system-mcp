# config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY or not TAVILY_API_KEY:
    raise ValueError("API keys for OpenAI and Tavily not found in .env file.")

ORCHESTRATOR_MODEL = "gpt-4"
ANALYST_MODEL = "gpt-4"
RESEARCHER_MODEL = "gpt-4"

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)