
# cli.py
import argparse
import importlib
import os
import shutil
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv
load_dotenv()

# Fix for ModuleNotFoundError when running from the root directory
sys.path.append('.')

BASE = Path(__file__).parent
TEMPLATE_DIR = BASE / "templates"
DEFAULT_LIBRARY = "agents_library"

def get_library_dir(dest: str = None):
    return BASE / (dest or DEFAULT_LIBRARY)

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
        sys.exit(1)

    shutil.copy(src, dest)
    print(f"✅ Added {kind}: {name} to {dest_dir}")

def list_all(dest_folder: str = None):
    print("\n=== Available Templates ===")
    print("Nodes:")
    for node in templates_available("node"):
        print(f"  - {node}")
    print("Workflows:")
    for wf in templates_available("workflow"):
        print(f"  - {wf}")

    print("\n=== Your Library ===")
    print("Nodes:")
    for node in library_items("node", dest_folder):
        print(f"  - {node}")
    print("Workflows:")
    for wf in library_items("workflow", dest_folder):
        print(f"  - {wf}")

def run_workflow(name: str, inputs: dict, dest_folder: str = None):
    lib_folder = dest_folder or DEFAULT_LIBRARY
    lib_dir = get_library_dir(dest_folder)
    if not lib_dir.exists():
        print(f"❌ The library folder '{lib_folder}' does not exist. Please scaffold your nodes/workflows first using the CLI 'add' command.")
        return
    module_name = f"{lib_folder}.workflows.{name}"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"❌ Could not import workflow '{name}' from '{lib_folder}': {e}")
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

def main(argv: List[str] = None):
    parser = argparse.ArgumentParser(description="shadcn-agents CLI: Scaffold and run agent nodes/workflows from templates.\n\nYou must scaffold code into your own library folder (default: agents_library) before running or importing workflows.")
    sub = parser.add_subparsers(dest="cmd")

    parser_add = sub.add_parser("add", help="Scaffold a node or workflow from template into your library.")
    parser_add.add_argument("kind", choices=["node", "workflow"], help="Type of component to add.")
    parser_add.add_argument("name", help="Name of template (without .py)")
    parser_add.add_argument("--dest", default=None, help="Destination library folder (default: agents_library)")

    parser_list = sub.add_parser("list", help="List available templates and your library contents.")
    parser_list.add_argument("--dest", default=None, help="Library folder to list (default: agents_library)")


    parser_run = sub.add_parser("run", help="Run a workflow from your library.")
    parser_run.add_argument("kind", choices=["workflow"], help="Type of component to run (only workflow supported).")
    parser_run.add_argument("name", help="Name of workflow to run.")
    parser_run.add_argument("--dest", default=None, help="Library folder to use (default: agents_library)")
    # Accept arbitrary key-value pairs for workflow inputs
    parser_run.add_argument("--inputs", nargs=argparse.REMAINDER, help="Additional workflow inputs as --key value pairs.")

    parser_playground = sub.add_parser("playground", help="Run the interactive playground app.")

    args = parser.parse_args(argv)

    if args.cmd == "add":
        add_component(args.kind, args.name, args.dest)
    elif args.cmd == "list":
        list_all(args.dest)
    elif args.cmd == "run":
        # Parse arbitrary --inputs as key-value pairs
        input_dict = {}
        if args.inputs:
            key = None
            for item in args.inputs:
                if item.startswith('--'):
                    key = item[2:]
                    input_dict[key] = None
                elif key:
                    input_dict[key] = item
                    key = None
        run_workflow(args.name, input_dict, args.dest)
    elif args.cmd == "playground":
        os.system("streamlit run playground.py")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()