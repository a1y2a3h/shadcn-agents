# shadcn-agent

[![PyPI version](https://badge.fury.io/py/shadcn-agent.svg)](https://badge.fury.io/py/shadcn-agent)
[![Python versions](https://img.shields.io/pypi/pyversions/shadcn-agent.svg)](https://pypi.org/project/shadcn-agent/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The shadcn for AI Agents** - A CLI tool that provides a collection of reusable, framework-native AI agent components with the same developer experience as shadcn/ui.

## 🌟 Features

- **📦 Fetch from GitHub:** Components are fetched directly from our GitHub repository - no need to clone anything
- **🔧 Atomic and Composable:** Get individual agent "nodes" (e.g., web scraper, summarizer, translator) that combine into powerful workflows
- **🕸️ Built for LangGraph:** Components use LangGraph's graph-based architecture for stateful, multi-step workflows
- **💻 Own Your Code:** CLI copies component code into your project - full control to modify, extend, and debug
- **🚀 Zero Dependencies:** No package lock-in once components are copied
- **🎮 Interactive Playground:** Test workflows with a web interface before deploying

---

## 🚀 Quick Start

### Installation

```bash
pip install shadcn-agent
```

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
│   ├── nodes/        # Individual agent nodes
│   └── workflows/    # Multi-node workflows
└── .env             # Your configuration
```

### 2. Add Components You Need

```bash
# Add individual nodes
shadcn-agent add node search_node
shadcn-agent add node summarizer_node
shadcn-agent add node translate_node
shadcn-agent add node email_node

# Add pre-built workflows
shadcn-agent add workflow summarize_and_email_graph
shadcn-agent add workflow translate_and_email_graph
```

### 3. Configure Environment

Create a `.env` file with your credentials:

```env
# Email configuration (for email workflows)
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your_app_password

# Default recipient for testing
DEFAULT_RECIPIENT=recipient@example.com

# Optional: Custom library folder
AGENTS_LIBRARY=components
```

### 4. Run Workflows

```bash
# Run workflows directly from CLI
shadcn-agent run workflow summarize_and_email_graph \
  --url "https://en.wikipedia.org/wiki/Large_language_model" \
  --recipient "your@email.com"

shadcn-agent run workflow translate_and_email_graph \
  --text "Hello, how are you?" \
  --target_lang "fr" \
  --recipient "your@email.com"
```

### 5. Interactive Playground

```bash
# Launch the web-based playground
shadcn-agent playground
```

Features:
- 🖥️ Test workflows with a GUI
- 🔧 **Custom Workflow Builder:** Drag-and-drop node combinations
- 💾 Download results as JSON
- 📊 Real-time execution monitoring

---

## 📚 Available Components

### Nodes
| Node | Description | Inputs | Outputs |
|------|-------------|---------|----------|
| **search_node** | Web scraper with BeautifulSoup | `url` | `text`, `scraped_url` |
| **summarizer_node** | Extractive text summarizer | `text` | `summary`, `word_count` |
| **translate_node** | Google Translate integration | `text`, `target_lang` | `translation` |
| **email_node** | SMTP email sender | `body`, `recipient` | `status` |

### Workflows
| Workflow | Description | Nodes Used |
|----------|-------------|------------|
| **summarize_and_email_graph** | Scrapes → Summarizes → Emails | search + summarizer + email |
| **translate_and_email_graph** | Translates → Emails | translate + email |
| **scrape_and_summarize_graph** | Scrapes → Summarizes | search + summarizer |

---

## 🛠️ CLI Commands

```bash
# Initialize project structure
shadcn-agent init [--dest folder_name] [--config]

# List available templates and your components
shadcn-agent list [--dest folder_name]

# Add components from GitHub
shadcn-agent add node <node_name> [--dest folder_name]
shadcn-agent add workflow <workflow_name> [--dest folder_name]

# Run workflows
shadcn-agent run workflow <workflow_name> [--dest folder_name] [args...]

# Launch interactive playground
shadcn-agent playground
```

## 🏗️ Custom Folder Structure

You can organize components in any folder structure:

```bash
# Use custom folder names
shadcn-agent init --dest my_agents
shadcn-agent add node search_node --dest my_agents
shadcn-agent run workflow summarize_and_email_graph --dest my_agents
```

---

## 💡 The "Own Your Code" Philosophy

Unlike traditional packages, shadcn-agent **copies** component code into your project:

```bash
shadcn-agent add node search_node
```

This creates `components/nodes/search_node.py` in **your project**. You can:

- ✅ **Modify** the code however you want
- ✅ **Debug** with full visibility into execution
- ✅ **Add** custom error handling and logging
- ✅ **Change** APIs, prompts, or business logic
- ✅ **Version control** your modifications
- ✅ **No dependency** on shadcn-agent after copying

---

## 🧩 Framework Integration

All components are built for **LangGraph**, ensuring:

- 🔄 **Native state management** between nodes
- 📊 **Graph-based workflow orchestration**
- 🔗 **Easy composition** and extension
- 🛡️ **Type-safe** state passing
- 📈 **Built-in monitoring** and debugging

Example of a custom workflow:

```python
from langgraph.graph import StateGraph, END
from components.nodes.search_node import search_node
from components.nodes.summarizer_node import summarizer_node

def build_custom_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)
    
    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", END)
    
    return workflow.compile()
```

---

## 🔧 Email Configuration

For email workflows, you need to configure SMTP credentials:

### Gmail Setup (Recommended)

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to [Google Account settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

3. Add to your `.env` file:
```env
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your_16_digit_app_password
```

### Other Email Providers

The email node supports any SMTP server. Modify the `email_node.py` after copying to use different SMTP settings.

---

## 🧪 Development & Testing

### Running Tests

```bash
# Install development dependencies
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=shadcn_agent --cov-report=html
```

### Development Setup

```bash
# Clone repository
git clone https://github.com/Aryan-Bagale/shadcn-agents.git
cd shadcn-agents

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run the playground locally
shadcn-agent playground
```

---

## 🐳 Docker Support

```bash
# Build and run with Docker
docker-compose up playground

# Development environment
docker-compose run dev bash
```

---

## 🚨 Troubleshooting

### Common Issues

#### "Import Error: Could not import workflow"
```bash
# Make sure all required nodes are added
shadcn-agent add node search_node
shadcn-agent add node summarizer_node
shadcn-agent add node email_node
```

#### "Email authentication failed"
- Verify your Gmail App Password (not regular password)
- Check that 2FA is enabled on your Google account
- Ensure `SENDER_EMAIL` and `SENDER_PASSWORD` are in `.env`

#### "Library folder not found"
```bash
# Initialize the project first
shadcn-agent init --dest components
```

#### "Workflow validation failed"
```bash
# Check required parameters for each workflow:
shadcn-agent run workflow summarize_and_email_graph --url "https://example.com"
shadcn-agent run workflow translate_and_email_graph --text "Hello" --target_lang "fr"
```

### Debug Mode

Enable detailed error messages:

```env
DEBUG=true
```

### Network Issues

If you're behind a corporate firewall:

```bash
# Use HTTP instead of HTTPS for GitHub (not recommended for production)
export GITHUB_REPO="http://raw.githubusercontent.com/Aryan-Bagale/shadcn-agents"
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Adding New Components

1. Create templates in the `templates/` directory
2. Follow the LangGraph node/workflow patterns
3. Add comprehensive error handling
4. Include tests for your components
5. Submit a pull request

### Component Guidelines

- **Nodes:** Should be pure functions that take and return state dictionaries
- **Error Handling:** Always handle failures gracefully and return meaningful error messages
- **Documentation:** Include docstrings and type hints
- **Testing:** Add unit tests in the `tests/` directory

### Development Workflow

```bash
# Fork the repository
git fork https://github.com/Aryan-Bagale/shadcn-agents.git

# Create a feature branch
git checkout -b feature/new-component

# Make your changes
# ...

# Run tests
pytest tests/

# Format code
black shadcn_agent/
flake8 shadcn_agent/

# Commit and push
git commit -m "Add new component"
git push origin feature/new-component

# Create pull request
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Homepage:** [https://github.com/Aryan-Bagale/shadcn-agents](https://github.com/Aryan-Bagale/shadcn-agents)
- **PyPI:** [https://pypi.org/project/shadcn-agent/](https://pypi.org/project/shadcn-agent/)
- **Documentation:** [GitHub README](https://github.com/Aryan-Bagale/shadcn-agents#readme)
- **Issues:** [GitHub Issues](https://github.com/Aryan-Bagale/shadcn-agents/issues)

---

## ⭐ Show Your Support

If shadcn-agent helps you build better AI workflows, please consider:

- ⭐ **Starring** the repository
- 🐛 **Reporting bugs** and feature requests
- 🔧 **Contributing** new components
- 📢 **Sharing** with the community

Made with ❤️ by [Aryan Bagale](https://github.com/Aryan-Bagale)