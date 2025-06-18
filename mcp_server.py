# mcp_server.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes
from agents import system_analyst_agent, cybersecurity_researcher_agent
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="System Guardian MCP Server",
    version="1.0",
    description="A server hosting specialized AI agents for system analysis and security research.",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

add_routes(
    app,
    system_analyst_agent,
    path="/system-analyst",
)

add_routes(
    app,
    cybersecurity_researcher_agent,
    path="/cyber-researcher",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, log_level="debug")