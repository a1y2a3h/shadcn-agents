# shadcn-agent
The Shadcn for AI Agents
shadcn-agent is a CLI-driven library that provides a collection of reusable, framework-native AI agent components. Inspired by the developer experience of shadcn/ui, it gives you the building blocks for complex, stateful workflows that are yours to own and customize.

Stop copying code from tutorials. Use the shadcn-agent CLI to add production-ready components directly to your project.

Why shadcn-agent?
Atomic and Composable: Get individual agent "nodes" (e.g., a summarizer, a web scraper) that can be easily combined into powerful, multi-step workflows.

Built for LangGraph: Components are built directly for the LangGraph framework, ensuring seamless integration and compatibility with its graph-based architecture.

Own Your Code: The CLI copies the component code into your project, giving you full control to modify, extend, and debug it without waiting for an upstream update.

Intuitive CLI: A simple command-line interface makes it easy to add new components and get started in seconds.

Quick Start
1. Project Setup
Create a new folder and set up a basic Python environment.

Bash

mkdir shadcn-agent
cd shadcn-agent
pip install langgraph
2. Install the CLI
Copy the cli.py and templates/ folders directly into your project.

3. Add Components
Use the CLI to add the core nodes and a sample workflow.

Bash

python cli.py add node summarizer_node
python cli.py add workflow summarize_and_email_graph
4. Run the Demo
Create a main.py file to demonstrate your new workflow.

Python

# main.py
from agents_library.workflows.summarize_and_email_graph import build_summarize_and_email_graph

if __name__ == "__main__":
    graph = build_summarize_and_email_graph()

    print("🚀 Running Summarize + Email Workflow...\n")
    inputs = {"input": "LangGraph makes it easier to build stateful AI workflows with reusable components."}

    for step in graph.stream(inputs):
        print("Step Output:", step)

    print("\n✅ Workflow complete!")
Run the demo to see it in action.

Bash

python main.py

Contributing
We welcome contributions! If you have an idea for a new node or a bug fix, please open an issue or submit a pull request on GitHub.