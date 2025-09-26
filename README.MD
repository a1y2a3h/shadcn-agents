# shadcn-agent

The Shadcn for AI Agents

shadcn-agent is a CLI tool that provides a collection of reusable, framework-native AI agent components. Inspired by the developer experience of shadcn/ui, it gives you the building blocks for complex, stateful workflows that are yours to own and customize.

**Why shadcn-agent?**
- **Fetch from GitHub:** Components are fetched directly from our GitHub repository - no need to clone anything
- **Atomic and Composable:** Get individual agent "nodes" (e.g., a summarizer, a web scraper) that can be easily combined into powerful, multi-step workflows
- **Built for LangGraph:** Components are built directly for the LangGraph framework, ensuring seamless integration and compatibility with its graph-based architecture
- **Own Your Code:** The CLI copies component code into your project, giving you full control to modify, extend, and debug it
- **Zero Dependencies:** No package lock-in - once you've copied components, you can modify them freely

---

## Installation

```bash
pip install shadcn-agent
```

## Quick Start

### 1. Initialize Your Project

```bash
# Create a new directory for your AI project
mkdir my-ai-project
cd my-ai-project

# Initialize shadcn-agent structure
shadcn-agent init
```

This creates:
```
my-ai-project/
├── components/
│   ├── nodes/
│   └── workflows/
└── .shadcn-agent.json  # Optional config
```

### 2. Add Components You Need

```bash
# Add individual nodes
shadcn-agent add node search_node
shadcn-agent add node summarizer_node
shadcn-agent add node email_node
shadcn-agent add node translate_node

# Add pre-built workflows
shadcn-agent add workflow summarize_and_email_graph
shadcn-agent add workflow translate_and_email_graph
shadcn-agent add workflow scrape_and_summarize_graph
```

### 3. Set Up Environment

Create a `.env` file with your email credentials:

```env
SENDER_EMAIL=your@email.com
SENDER_PASSWORD=your_app_password
```

### 4. Run Workflows

```bash
# Run a workflow directly from CLI
shadcn-agent run workflow summarize_and_email_graph --url "https://en.wikipedia.org/wiki/Large_language_model" --recipient "your@email.com"

shadcn-agent run workflow translate_and_email_graph --text "Hello, how are you?" --target_lang "fr" --recipient "your@email.com"

shadcn-agent run workflow scrape_and_summarize_graph --url "https://en.wikipedia.org/wiki/Artificial_intelligence"
```

### 5. Run the Interactive Playground

```bash
shadcn-agent playground
```

- Test workflows with a web interface
- **Custom Workflow Builder:** Select and order any nodes to build your own workflow
- Download results as JSON

---

## Custom Folder Names

You can organize components in any folder structure:

```bash
# Use custom folder names
shadcn-agent init --dest my_agents
shadcn-agent add node search_node --dest my_agents
shadcn-agent run workflow summarize_and_email_graph --dest my_agents --url "https://example.com"
```

## Available Components

### Nodes
- **search_node** - Web scraper with BeautifulSoup
- **summarizer_node** - Text summarizer
- **translate_node** - Language translator using Google Translate
- **email_node** - Email sender with SMTP

### Workflows
- **summarize_and_email_graph** - Scrapes → Summarizes → Emails
- **translate_and_email_graph** - Translates → Emails  
- **scrape_and_summarize_graph** - Scrapes → Summarizes

## The "Own Your Code" Philosophy

Unlike traditional packages, shadcn-agent **copies** component code into your project:

```bash
shadcn-agent add node search_node
```

This creates `components/nodes/search_node.py` in **your project**. You can:
- ✅ Modify the code however you want
- ✅ Debug with full visibility
- ✅ Add custom error handling
- ✅ Change APIs, prompts, or logic
- ✅ Version control your modifications
- ✅ No dependency on shadcn-agent after copying

## Commands

```bash
# Initialize project structure
shadcn-agent init [--dest folder_name] [--config]

# List available templates and your components  
shadcn-agent list [--dest folder_name]

# Add components from GitHub
shadcn-agent add node <node_name> [--dest folder_name]
shadcn-agent add workflow <workflow_name> [--dest folder_name]

# Run workflows
shadcn-agent run workflow <workflow_name> [--dest folder_name] [--url URL] [--text TEXT] [--target_lang LANG] [--recipient EMAIL]

# Launch interactive playground
shadcn-agent playground
```

## Framework Integration

All components are built for **LangGraph**, ensuring:
- Native state management
- Graph-based workflow orchestration  
- Easy composition and extension
- Type-safe state passing between nodes

## Contributing

We welcome contributions! Add new nodes or workflows by:
1. Creating templates in the `templates/` directory
2. Following the LangGraph node/workflow patterns
3. Submitting a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.