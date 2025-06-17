import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY or not TAVILY_API_KEY:
    raise ValueError("API keys for OpenAI and Tavily not found in .env file.")

# --- Model Configuration ---
ORCHESTRATOR_MODEL = "gpt-4o"
ANALYST_MODEL = "gpt-4o"
RESEARCHER_MODEL = "gpt-4o"

# --- File Paths and Directories ---
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)