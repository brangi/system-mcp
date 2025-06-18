from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langserve import RemoteRunnable
from langchain_core.prompts import PromptTemplate

import config
from tools import list_running_processes, search_web_for_vulnerabilities, read_file_content

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str) -> AgentExecutor:
    # Create a prompt template that handles both initial input and intermediate steps
    prompt = PromptTemplate.from_template(
        """You are a helpful assistant that executes tasks using the provided tools.

Available tools:
{tools}

Tool names: {tool_names}

To use a tool, follow this format:
Thought: Consider what needs to be done
Action: The name of the tool to use
Action Input: The input for the tool
Observation: The result of the tool
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: The final answer to the original input question

Task: {input}

{agent_scratchpad}"""
    )
    
    # Create the agent with the prompt
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the executor with proper error handling
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10  # Prevent infinite loops
    )

analyst_llm = ChatOpenAI(model=config.ANALYST_MODEL, temperature=0)
analyst_tools = [
    Tool(name="List Running Processes", func=list_running_processes, description="A tool to list all running processes on the local machine."),
    Tool(name="Read File Content", func=read_file_content, description="A tool to read the contents of a specific file within the project directory."),
]
analyst_system_prompt = "You are a meticulous System Analyst Agent. Your sole purpose is to execute tasks using the tools provided to inspect the local system. Provide clear, factual reports based ONLY on the output of your tools."
system_analyst_agent = create_agent(analyst_llm, analyst_tools, analyst_system_prompt)

researcher_llm = ChatOpenAI(model=config.RESEARCHER_MODEL, temperature=0)
researcher_tools = [
    Tool(name="Search Web for Vulnerabilities", func=search_web_for_vulnerabilities, description="A tool to search the web for vulnerabilities related to a given software name."),
]
researcher_system_prompt = "You are a Cybersecurity Researcher Agent. Your mission is to find threats and vulnerabilities. You will be given the names of software or processes and must find any known security issues (like CVEs) or misconfigurations."
cybersecurity_researcher_agent = create_agent(researcher_llm, researcher_tools, researcher_system_prompt)

remote_analyst_tool = RemoteRunnable("http://localhost:8000/system-analyst")
remote_researcher_tool = RemoteRunnable("http://localhost:8000/cyber-researcher")

def run_system_analyst_remotely(task: str) -> str:
    """Run the System Analyst agent remotely."""
    try:
        # Create the remote tool with proper input handling
        remote_analyst_tool = RemoteRunnable(url="http://localhost:8000/system-analyst")
        
        # Ensure we're passing the input correctly
        response = remote_analyst_tool.invoke({
            "input": task,
            "agent_scratchpad": ""  # Initialize empty scratchpad
        })
        return response
    except Exception as e:
        return f"Error running System Analyst: {str(e)}"

def run_cybersecurity_researcher_remotely(software_name: str) -> str:
    """Run the Cybersecurity Researcher agent remotely."""
    try:
        # Create the remote tool with proper input handling
        remote_researcher_tool = RemoteRunnable(url="http://localhost:8000/cybersecurity-researcher")
        
        # Ensure we're passing the input correctly
        response = remote_researcher_tool.invoke({
            "input": software_name,
            "agent_scratchpad": ""  # Initialize empty scratchpad
        })
        return response
    except Exception as e:
        return f"Error running Cybersecurity Researcher: {str(e)}"

orchestrator_llm = ChatOpenAI(model=config.ORCHESTRATOR_MODEL, temperature=0)
orchestrator_tools = [
    Tool.from_function(
        func=run_system_analyst_remotely,
        name="System Analyst",
        description="Use this specialist to inspect the local system. Pass it a clear, single-string instruction for the task you want it to perform.",
    ),
    Tool.from_function(
        func=run_cybersecurity_researcher_remotely,
        name="Cybersecurity Researcher",
        description="Use this specialist to find security vulnerabilities. Pass it the single name of the software you want it to research.",
    ),
]
orchestrator_system_prompt = "You are the Orchestrator, the master agent. Your goal is to fulfill the user's request by creating a plan and delegating tasks to your specialist agents. Analyze the plan, delegate, synthesize the results, and create a final comprehensive report."
orchestrator_agent = create_agent(orchestrator_llm, orchestrator_tools, orchestrator_system_prompt)