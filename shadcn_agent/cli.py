# cli.py

import argparse
import importlib
import os
import sys
import requests
from pathlib import Path
from typing import List, Dict
import tempfile
import json
import subprocess

# GitHub repository configuration
GITHUB_REPO = "Aryan-Bagale/shadcn-agents"
GITHUB_BRANCH = "main"
TEMPLATES_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/templates"

def fetch_template_content(kind: str, name: str) -> str:
    """Fetch template content directly from GitHub"""
    url = f"{TEMPLATES_BASE_URL}/{kind}s/{name}.py"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch template from {url}: {e}")

def fetch_available_templates() -> Dict[str, List[str]]:
    """Fetch list of available templates from GitHub API"""
    try:
        # Fetch nodes
        nodes_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/templates/nodes"
        nodes_response = requests.get(nodes_url)
        nodes_response.raise_for_status()
        nodes = [item['name'].replace('.py', '') for item in nodes_response.json() if item['name'].endswith('.py')]
        
        # Fetch workflows
        workflows_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/templates/workflows"
        workflows_response = requests.get(workflows_url)
        workflows_response.raise_for_status()
        workflows = [item['name'].replace('.py', '') for item in workflows_response.json() if item['name'].endswith('.py')]
        
        return {"nodes": nodes, "workflows": workflows}
    except requests.RequestException as e:
        print(f"⚠️  Could not fetch template list from GitHub: {e}")
        print("📡 Using fallback template list...")
        # Fallback list of known templates
        return {
            "nodes": ["search_node", "summarizer_node", "translate_node", "email_node"],
            "workflows": ["summarize_and_email_graph", "translate_and_email_graph", "scrape_and_summarize_graph"]
        }

def get_library_dir(dest: str = None):
    return Path(dest or "components")

def library_items(kind: str, dest: str = None) -> List[str]:
    p = get_library_dir(dest) / (kind + "s")
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.py")]

def add_component(kind: str, name: str, dest_folder: str = None):
    """Add a component by fetching it from GitHub"""
    dest_dir = get_library_dir(dest_folder) / (kind + "s")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{name}.py"

    if dest.exists():
        print(f"⚠️  {name}.py already exists in {dest_dir}/")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(1)

    try:
        print(f"📡 Fetching {kind} template: {name}...")
        content = fetch_template_content(kind, name)
        
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Added {kind}: {name} to {dest_dir}")
    except Exception as e:
        print(f"❌ Failed to add {kind} '{name}': {e}")
        sys.exit(1)

def list_all(dest_folder: str = None):
    lib_name = dest_folder or "components"
    
    print("📡 Fetching available templates...")
    available = fetch_available_templates()
    
    print("\n=== Available Templates (from GitHub) ===")
    print("Nodes:")
    for node in available["nodes"]:
        print(f"  - {node}")
    print("Workflows:")
    for wf in available["workflows"]:
        print(f"  - {wf}")

    print(f"\n=== Your {lib_name}/ Library ===")
    print("Nodes:")
    for node in library_items("node", dest_folder):
        print(f"  - {node}")
    print("Workflows:")
    for wf in library_items("workflow", dest_folder):
        print(f"  - {wf}")

def run_workflow(name: str, inputs: dict, dest_folder: str = None):
    lib_folder = dest_folder or "components"
    lib_dir = get_library_dir(dest_folder)
    
    if not lib_dir.exists():
        print(f"❌ The library folder '{lib_folder}' does not exist.")
        print(f"💡 Initialize it with: shadcn-agent init --dest {lib_folder}")
        return

    # Dynamically add the user's project folder to the path
    sys.path.insert(0, str(lib_dir.parent))
    
    module_name = f"{lib_folder}.workflows.{name}"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"❌ Could not import workflow '{name}' from '{lib_folder}': {e}")
        print(f"💡 Make sure you've added it: shadcn-agent add workflow {name} --dest {lib_folder}")
        return

    builder = getattr(mod, "build_workflow", None)
    if builder is None:
        print(f"❌ Workflow module {module_name} does not expose build_workflow()")
        return

    app = builder()
    print(f"🚀 Running workflow: {name} from {lib_folder}")
    for step in app.stream(inputs):
        print("Step Output:", step)
    print("✅ Done")

def init_project(dest_folder: str = None):
    """Initialize a new shadcn-agent project with basic structure"""
    lib_folder = dest_folder or "components"
    lib_dir = get_library_dir(dest_folder)
    
    # Create the directory structure
    (lib_dir / "nodes").mkdir(parents=True, exist_ok=True)
    (lib_dir / "workflows").mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files to make it a proper Python package
    (lib_dir / "__init__.py").touch()
    (lib_dir / "nodes" / "__init__.py").touch()
    (lib_dir / "workflows" / "__init__.py").touch()
    
    print(f"✅ Initialized shadcn-agent project structure in {lib_folder}/")
    print(f"📁 Created: {lib_folder}/nodes/ and {lib_folder}/workflows/")
    print(f"💡 Next: shadcn-agent add node <node_name> --dest {lib_folder}")


def run_playground():
    """Run the shadcn-agent playground using the packaged version"""
    try:
        # Get the path to the packaged playground.py
        package_dir = Path(__file__).parent
        playground_path = package_dir / "playground.py"
        
        if not playground_path.exists():
            print("❌ Playground not found in package. Please reinstall shadcn-agent.")
            sys.exit(1)
        
        print("🚀 Starting shadcn-agent playground...")
        print(f"📁 Looking for components in current directory")
        print("💡 Tip: Run this in a directory with your shadcn-agent components")
        
        # Run streamlit with the packaged playground
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(playground_path),
            "--server.headless", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Playground stopped.")
    except FileNotFoundError:
        print("❌ Streamlit not found. Install it with: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start playground: {e}")
        sys.exit(1)



def create_config(dest_folder: str = None):
    """Create a .shadcn-agent.json config file"""
    config = {
        "components_dir": dest_folder or "components",
        "github_repo": GITHUB_REPO,
        "github_branch": GITHUB_BRANCH
    }
    
    with open('.shadcn-agent.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created .shadcn-agent.json config file")

def main(argv: List[str] = None):
    parser = argparse.ArgumentParser(
        description="shadcn-agent: Build composable AI agents with copy-paste components from GitHub.",
        epilog="Examples:\n"
               "  shadcn-agent init --dest my_agents\n"
               "  shadcn-agent add node summarizer_node --dest my_agents\n"
               "  shadcn-agent add workflow summarize_and_email_graph --dest my_agents\n"
               "  shadcn-agent run workflow summarize_and_email_graph --dest my_agents --url https://example.com",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd")

    # Init command
    parser_init = sub.add_parser("init", help="Initialize a new shadcn-agent project structure.")
    parser_init.add_argument("--dest", default=None, help="Destination folder (default: components)")
    parser_init.add_argument("--config", action="store_true", help="Create .shadcn-agent.json config file")

    # Add command
    parser_add = sub.add_parser("add", help="Add a node or workflow template from GitHub to your project.")
    parser_add.add_argument("kind", choices=["node", "workflow"], help="Type of component to add.")
    parser_add.add_argument("name", help="Name of template (without .py)")
    parser_add.add_argument("--dest", default=None, help="Destination folder (default: components)")

    # List command
    parser_list = sub.add_parser("list", help="List available templates from GitHub and your project components.")
    parser_list.add_argument("--dest", default=None, help="Project folder to list (default: components)")

    # Run command
    parser_run = sub.add_parser("run", help="Run a workflow from your project.")
    parser_run.add_argument("kind", choices=["workflow"], help="Type of component to run.")
    parser_run.add_argument("name", help="Name of workflow to run.")
    parser_run.add_argument("--dest", default=None, help="Project folder (default: components)")
    parser_run.add_argument("--url", default=None, help="URL input for the workflow.")
    parser_run.add_argument("--text", default=None, help="Text input for the workflow.")
    parser_run.add_argument("--target_lang", default=None, help="Target language (for translate workflows).")
    parser_run.add_argument("--recipient", default=None, help="Recipient email (optional).")

    # Playground command
    parser_playground = sub.add_parser("playground", help="Run the interactive playground app.")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        init_project(args.dest)
        if args.config:
            create_config(args.dest)
    elif args.cmd == "add":
        add_component(args.kind, args.name, args.dest)
    elif args.cmd == "list":
        list_all(args.dest)
    elif args.cmd == "run":
        inputs = {
            "url": args.url,
            "text": args.text,
            "target_lang": args.target_lang,
            "recipient": args.recipient,
        }
        inputs = {k: v for k, v in inputs.items() if v is not None}
        
        if args.name == "summarize_and_email_graph" and "url" not in inputs:
            print("❌ Error: 'summarize_and_email_graph' workflow requires a --url input.")
            sys.exit(1)
        if args.name == "translate_and_email_graph" and "text" not in inputs:
            print("❌ Error: 'translate_and_email_graph' workflow requires a --text input.")
            sys.exit(1)

        run_workflow(args.name, inputs, args.dest)
    elif args.cmd == "playground":
    run_playground())

if __name__ == "__main__":
    main()