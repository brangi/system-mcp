# tools.py

import os
import psutil
from langchain_tavily import TavilySearch
import config

def list_running_processes(*args, **kwargs) -> str:
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info'])
            if pinfo['memory_info']:
                pinfo['memory_mb'] = pinfo['memory_info'].rss / (1024 * 1024)
                processes.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    report = "Running Processes:\n"
    report += "-"*50 + "\n"
    report += f"{'PID':<10}{'Name':<25}{'CPU%':<10}{'Memory(MB)':<10}\n"
    report += "-"*50 + "\n"
    for p in sorted(processes, key=lambda i: i['memory_mb'], reverse=True)[:25]:
        report += (f"{p['pid']:<10}{p['name']:<25.25}"
                   f"{p['cpu_percent']:<10.2f}"
                   f"{p['memory_mb']:<10.2f}\n")
    return report

tavily_tool = TavilySearch(
    max_results=5,
    tavily_api_key=config.TAVILY_API_KEY
)

def search_web_for_vulnerabilities(software_name: str) -> str:
    print(f"--- Searching for vulnerabilities related to: {software_name} ---")
    query = f'security vulnerabilities and exploits for "{software_name}"'
    return tavily_tool.invoke({"query": query})

def read_file_content(filepath: str) -> str:
    project_root = os.path.abspath(os.path.dirname(__file__))
    target_path = os.path.abspath(filepath)
    if not target_path.startswith(project_root):
        return "Error: Access Denied. Can only read files within the project directory."
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)
            if len(content) == 2000:
                return content + "\n\n... (file truncated)"
            return content
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"