# shadcn-agent
The Shadcn for AI Agents
shadcn-agent is a CLI-driven library that provides a collection of reusable, framework-native AI agent components. Inspired by the developer experience of shadcn/ui, it gives you the building blocks for complex, stateful workflows that are yours to own and customize.

Stop copying code from tutorials. Use the shadcn-agent CLI to add production-ready components directly to your project.

Why shadcn-agent?
Atomic and Composable: Get individual agent "nodes" (e.g., a summarizer, a web scraper) that can be easily combined into powerful, multi-step workflows.

Built for LangGraph: Components are built directly for the LangGraph framework, ensuring seamless integration and compatibility with its graph-based architecture.

Own Your Code: The CLI copies the component code into your project, giving you full control to modify, extend, and debug it without waiting for an upstream update.

Intuitive CLI: A simple command-line interface makes it easy to add new components and get started in seconds.


## Quick Start

### 1. Project Setup
Create a new folder and set up a basic Python environment.

```bash
mkdir shadcn-agent
cd shadcn-agent
pip install langgraph streamlit deep-translator beautifulsoup4 requests python-dotenv
```

### 2. Install the CLI
Copy the `cli.py` and `templates/` folders directly into your project.

### 3. Add Components
Use the CLI to add nodes and workflows:

```bash
python cli.py add node summarizer_node
python cli.py add node search_node
python cli.py add node translate_node
python cli.py add node email_node
python cli.py add workflow summarize_and_email_graph
python cli.py add workflow translate_and_email_graph
python cli.py add workflow scrape_and_summarize_graph
```

### 4. Run the Playground (Recommended)
Launch the interactive web playground:

```bash
python cli.py playground
```
Select a workflow, enter your inputs, and see live results in your browser!

### 5. Run a Workflow from the CLI
You can also run workflows directly:

```bash
python cli.py run workflow summarize_and_email_graph --text "https://en.wikipedia.org/wiki/Artificial_intelligence" --recipient "test@example.com"
python cli.py run workflow translate_and_email_graph --text "Hello, how are you?" --target_lang "fr" --recipient "test@example.com"
python cli.py run workflow scrape_and_summarize_graph --text "https://en.wikipedia.org/wiki/Artificial_intelligence"
```

## Workflows
- **Summarize + Email**: Scrapes a URL, summarizes the content, and emails the result.
- **Translate + Email**: Translates text to a target language and emails the result.
- **Scrape + Summarize**: Scrapes a URL and summarizes the content.

## Playground Demo
![Playground Screenshot](playground_screenshot.png)

## Contributing
We welcome contributions! If you have an idea for a new node or a bug fix, please open an issue or submit a pull request on GitHub.

Contributing
We welcome contributions! If you have an idea for a new node or a bug fix, please open an issue or submit a pull request on GitHub.