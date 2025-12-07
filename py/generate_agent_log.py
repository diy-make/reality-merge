import argparse
import datetime
import json

class LogEntry:
    def __init__(self, timestamp, action, discovery=None, commit=None, reasoning=None):
        self.timestamp = timestamp
        self.action = action
        self.discovery = discovery
        self.commit = commit
        self.reasoning = reasoning

    def to_markdown(self):
        md = f"-   **Timestamp:** {self.timestamp}\n"
        md += f"-   **Action:** {self.action}\n"
        if self.discovery:
            md += f"-   **Discovery:** {self.discovery}\n"
        if self.commit:
            md += f"-   **Commit `{self.commit}`:**\n" # Placeholder for commit message
        if self.reasoning:
            md += f"-   **Reasoning:** {self.reasoning}\n"
        return md

def main():
    # The theory is that some of this is not deterministic and you need to use induction.
    # The agent should review the generated markdown and make it more human-readable.
    parser = argparse.ArgumentParser(description="Generate an agent's work summary log.")
    parser.add_argument("--agent-name", required=True, help="The name of the agent.")
    parser.add_argument("--log-file", required=True, help="Path to a JSON file containing the log entries.")
    args = parser.parse_args()

    with open(args.log_file, 'r') as f:
        log_data = json.load(f)

    log_entries = [LogEntry(**entry) for entry in log_data["entries"]]

    full_markdown = f"# Work Summary: {args.agent_name} & User\n\n"
    full_markdown += f"This document summarizes the work completed by the AI agent **{args.agent_name}** in collaboration with the user on **{datetime.date.today().strftime('%B %d, %Y')}**.\n\n"

    for section, entries in log_data["sections"].items():
        full_markdown += f"## {section}\n\n"
        for entry_index in entries:
            full_markdown += log_entries[entry_index].to_markdown() + "\n"

    with open(f"md/{args.agent_name}.md", "w") as f:
        f.write(full_markdown)

if __name__ == "__main__":
    main()
