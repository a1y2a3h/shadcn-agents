# cli.py

import argparse
import importlib
import os
import shutil
import sys
from pathlib import Path
from typing import List

# Fix for ModuleNotFoundError when running from the root directory
sys.path.append('.')

BASE = Path(__file__).parent
TEMPLATE_DIR = BASE / "templates"

def get_library_dir(dest: str = None):
    # Default to 'components' to be more shadcn-like, but allow customization
    return Path(dest or "components")

def templates_available(kind: str) -> List[str]:
    p = TEMPLATE_DIR / (kind + "s")
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.py")]

def library_items(kind: str, dest: str = None) -> List[str]:
    p = get_library_dir(dest) / (kind + "s")
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.py")]

def add_component(kind: str, name: str, dest_folder: str = None):
    src = TEMPLATE_DIR / (kind + "s") / f"{name}.py"
    dest_dir = get_library_dir(dest_folder) / (kind + "s")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{name}.py"

    if not src.exists():
        print(f"❌ Template not found: {src}")
        sys.exit(1)
    if dest.exists():
        print(f"⚠️ {name}.py already exists in {dest_dir}/")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            sys.exit(1)

    shutil.copy(src, dest)
    print(f"✅ Added {kind}: {name} to {dest_dir}")

def list_all(dest_folder: str = None):
    lib_name = dest_folder or "components"
    
    print("\n=== Available Templates ===")
    print("Nodes:")
    for node in templates_available("node"):
        print(f"  - {node}")
    print("Workflows:")
    for wf in templates_available("workflow"):
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
        print(f"💡 Initialize it with: python cli.py add workflow {name} --dest {lib_folder}")
        return

    # Dynamically add the user's project folder to the path
    sys.path.insert(0, str(lib_dir.parent))
    
    module_name = f"{lib_folder}.workflows.{name}"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"❌ Could not import workflow '{name}' from '{lib_folder}': {e}")
        print(f"💡 Make sure you've added it: python cli.py add workflow {name} --dest {lib_folder}")
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
    print(f"💡 Next: python cli.py add node <node_name> --dest {lib_folder}")

def main(argv: List[str] = None):
    parser = argparse.ArgumentParser(
        description="shadcn-agent CLI: Build composable AI agents with copy-paste components.",
        epilog="Examples:\n"
               "  python cli.py init --dest my_agents\n"
               "  python cli.py add node summarizer_node --dest my_agents\n"
               "  python cli.py add workflow summarize_and_email_graph --dest my_agents\n"
               "  python cli.py run workflow summarize_and_email_graph --dest my_agents --url https://example.com",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="cmd")

    # Init command
    parser_init = sub.add_parser("init", help="Initialize a new shadcn-agent project structure.")
    parser_init.add_argument("--dest", default=None, help="Destination folder (default: components)")

    # Add command
    parser_add = sub.add_parser("add", help="Add a node or workflow template to your project.")
    parser_add.add_argument("kind", choices=["node", "workflow"], help="Type of component to add.")
    parser_add.add_argument("name", help="Name of template (without .py)")
    parser_add.add_argument("--dest", default=None, help="Destination folder (default: components)")

    # List command
    parser_list = sub.add_parser("list", help="List available templates and your project components.")
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
        os.system("streamlit run playground.py")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()