# System Guardian (system-mcp)

Designed to perform automated security and performance audits on a local computer system. It uses a team of specialized AI agents, orchestrated by a manager agent, to inspect system processes, research potential vulnerabilities online, and generate a comprehensive report.

## Features

- **Multi-Agent System:** Utilizes a hierarchical structure with an Orchestrator agent managing two specialist agents (System Analyst and Cybersecurity Researcher).
- **Deep System Inspection:** Can list and analyze running processes and their resource consumption using `psutil`.
- **Automated Vulnerability Research:** Leverages the Tavily search API to find real-time security information about software running on the system.
- **File System Access:** Includes a tool with safety guardrails to read local files within the project directory.
- **Configurable and Extensible:** Easily configure API keys and agent models in a dedicated file. New tools and agents can be added to extend functionality.

## Architecture

The application is built across four main Python files:

- **`config.py`**: A centralized file for all configurations, including API keys and AI model names.
- **`tools.py`**: Defines the capabilities of the agents, such as inspecting processes, searching the web, and reading files.
- **`agents.py`**: Contains the "personalities" and logic for each of the three agents (Orchestrator, System Analyst, Cybersecurity Researcher).
- **`main.py`**: The main entry point that starts the agent swarm and provides the high-level goal.

## Setup and Installation

**1. Clone or Create the Project Files**

**2. Create a Python Virtual Environment**

From your terminal, inside the project folder, create and activate a virtual environment. This is highly recommended to manage dependencies.

$ python -m venv venv

*Activate on Windows:*

$ .\venv\Scripts\activate

*Activate on macOS/Linux:*

$ source venv/bin/activate

**3. Create the Environment Variables File**

This project requires API keys for both OpenAI and Tavily (for web search).

Create a new file in the project root named `.env` and add your keys as follows:
```bash
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

- Get your OpenAI key from [platform.openai.com](https://platform.openai.com).
- Get your free Tavily key from [tavily.com](https://tavily.com).

**4. Install Dependencies**

Create a `requirements.txt` file with the content provided previously. Then, install all the necessary libraries with a single command:

$ pip install -r requirements.txt

## How to Run

With your virtual environment active and your `.env` file configured, simply run the `main.py` script:

$ python main.py

The application will start. It will take a few minutes to run as the agents think, plan, and delegate tasks. The verbose output will show you the entire collaborative process in real-time.

At the end, a final report will be printed to the console and saved as a `.txt` file in the `results/` directory.

## Customization

You can easily customize it:

- **Change the Goal:** Modify the `user_goal` variable in `main.py` to give the agent swarm a different objective.
- **Use Different Models:** Change the model names in `config.py` to use other models like `gpt-3.5-turbo` for the specialist agents to reduce cost.
- **Add New Tools:** Create new functions in `tools.py` and add them to the tool list of the appropriate agent in `agents.py`.

## TODO
- Add other models 
- Add a GUI
