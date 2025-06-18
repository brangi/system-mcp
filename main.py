
import datetime
from agents import orchestrator_agent
from config import RESULTS_DIR

def main():
    """
    The main function to run the System Guardian agent swarm.
    """
    print("--- Starting System Guardian Agent Swarm ---")

    user_goal = """
    Perform a basic security and performance audit on my system.
    First, get a list of all running processes.
    Then, for the top 5 processes by memory usage, ask the Cybersecurity Researcher
    to check for any known vulnerabilities.
    Finally, consolidate all findings into a detailed report.
    """

    print(f"Goal: {user_goal}")
    print("\n--- Orchestrator Agent is now running... ---")


    final_report = orchestrator_agent.invoke({"input": user_goal})

    print("\n--- Orchestrator Agent has finished its work. ---")
    print("\n\n--- FINAL REPORT ---")
    print(final_report['output'])


    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{RESULTS_DIR}/system_guardian_report_{timestamp}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(final_report['output'])

    print(f"\n--- Report has been saved to: {report_filename} ---")


if __name__ == "__main__":
    main()