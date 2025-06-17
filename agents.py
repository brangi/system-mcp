from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool

import config
from tools import list_running_processes, search_web_for_vulnerabilities, read_file_content

def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str) -> AgentExecutor:
    """Creates an agent executor with a given LLM, tools, and system prompt."""
    react_template = """
Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
    full_prompt_text = system_prompt + "\n\n" + react_template
    prompt = PromptTemplate.from_template(full_prompt_text)
    
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


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

def run_system_analyst(task: str) -> str:
    """
    Takes a string task and passes it to the System Analyst agent.
    The input to this tool should be a single string containing the full instruction for the System Analyst.
    """
    # The specialist agent expects its input in a dictionary like {"input": "task description"}
    response = system_analyst_agent.invoke({"input": task})
    return response['output']

def run_cybersecurity_researcher(software_name: str) -> str:
    """
    Takes a string software name and passes it to the Cybersecurity Researcher agent.
    The input to this tool should be a single string containing the name of the software to research.
    """
    response = cybersecurity_researcher_agent.invoke({"input": software_name})
    return response['output']


orchestrator_llm = ChatOpenAI(model=config.ORCHESTRATOR_MODEL, temperature=0)

# The Orchestrator's tools now use the new wrapper functions
orchestrator_tools = [
    Tool.from_function(
        func=run_system_analyst, # UPDATED
        name="System Analyst",
        description="Use this specialist to inspect the local system. Pass it a clear, single-string instruction for the task you want it to perform.",
    ),
    Tool.from_function(
        func=run_cybersecurity_researcher, # UPDATED
        name="Cybersecurity Researcher",
        description="Use this specialist to find security vulnerabilities. Pass it the single name of the software you want it to research.",
    ),
]

orchestrator_system_prompt = "You are the Orchestrator, the master agent. Your goal is to fulfill the user's request by creating a plan and delegating tasks to your specialist agents. Analyze the plan, delegate, synthesize the results, and create a final comprehensive report."
orchestrator_agent = create_agent(orchestrator_llm, orchestrator_tools, orchestrator_system_prompt)