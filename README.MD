
# shadcn-agent

The Shadcn for AI Agents

shadcn-agent is a CLI-driven library that provides a collection of reusable, framework-native AI agent components. Inspired by the developer experience of shadcn/ui, it gives you the building blocks for complex, stateful workflows that are yours to own and customize.

**Why shadcn-agent?**
- **Atomic and Composable:** Get individual agent "nodes" (e.g., a summarizer, a web scraper) that can be easily combined into powerful, multi-step workflows.
- **Built for LangGraph:** Components are built directly for the LangGraph framework, ensuring seamless integration and compatibility with its graph-based architecture.
- **Own Your Code:** The CLI copies the component code into your project, giving you full control to modify, extend, and debug it without waiting for an upstream update.
- **Intuitive CLI:** A simple command-line interface makes it easy to add new components and get started in seconds.

---

## Quick Start

### 1. Project Setup

```bash
mkdir shadcn-agent
cd shadcn-agent
pip install langgraph streamlit deep-translator beautifulsoup4 requests python-dotenv
```

### 2. Install the CLI

Copy the `cli.py` and `templates/` folders directly into your project.

### 3. Scaffold Components into Your Project

Use the CLI to copy node and workflow templates into your own `agents_library/` folder (or a custom folder):

```bash
python cli.py add node summarizer_node --dest agents_library
python cli.py add node search_node --dest agents_library
python cli.py add node translate_node --dest agents_library
python cli.py add node email_node --dest agents_library
python cli.py add workflow summarize_and_email_graph --dest agents_library
python cli.py add workflow translate_and_email_graph --dest agents_library
python cli.py add workflow scrape_and_summarize_graph --dest agents_library
```

> **Note:** You must scaffold nodes and workflows into your own library folder before running or importing them. The CLI will create this folder for you if it doesn't exist. You can also specify a custom destination folder with `--dest`.

### 4. Run the Playground (Recommended)

```bash
python cli.py playground
```

- Select your library folder in the sidebar (default: `agents_library`).
- Choose a workflow, enter your inputs, and see live results in your browser!
- **Custom Workflow Builder:** Select and order any nodes to build your own workflow. Download results as JSON.

### 5. Run a Workflow from the CLI

You can now pass any workflow input as a key-value pair using `--inputs`:

```bash
python cli.py run workflow summarize_and_email_graph --dest agents_library --inputs --url "https://en.wikipedia.org/wiki/Large_language_model" --recipient "your@email.com"
python cli.py run workflow translate_and_email_graph --dest agents_library --inputs --text "Hello, how are you?" --target_lang "fr" --recipient "your@email.com"
python cli.py run workflow scrape_and_summarize_graph --dest agents_library --inputs --url "https://en.wikipedia.org/wiki/Artificial_intelligence"
```

### 6. Environment Variables

Create a `.env` file in your project root with your email credentials:

```
SENDER_EMAIL=your@email.com
SENDER_PASSWORD=your_app_password
```

---

## Workflows

- **Summarize + Email:** Scrapes a URL, summarizes the content, and emails the result.
- **Translate + Email:** Translates text to a target language and emails the result.
- **Scrape + Summarize:** Scrapes a URL and summarizes the content.
- **Custom Workflow Builder:** Build your own workflow from available nodes in the playground UI.

---

## Contributing

We welcome contributions! If you have an idea for a new node or a bug fix, please open an issue or submit a pull request on GitHub.