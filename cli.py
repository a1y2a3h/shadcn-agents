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
LIBRARY_DIR = BASE / "agents_library"

def templates_available(kind: str) -> List[str]:
    p = TEMPLATE_DIR / (kind + "s")
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.py")]

def library_items(kind: str) -> List[str]:
    p = LIBRARY_DIR / (kind + "s")
    if not p.exists():
        return []
    return [f.stem for f in p.glob("*.py")]

def add_component(kind: str, name: str):
    src = TEMPLATE_DIR / (kind + "s") / f"{name}.py"
    dest_dir = LIBRARY_DIR / (kind + "s")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{name}.py"

    if not src.exists():
        print(f"❌ Template not found: {src}")
        sys.exit(1)
    if dest.exists():
        print(f"⚠️ {name}.py already exists in {kind}s/")
        sys.exit(1)

    shutil.copy(src, dest)
    print(f"✅ Added {kind}: {name}")

def list_all():
    print("\n=== Available Templates ===")
    print("Nodes:")
    for node in templates_available("node"):
        print(f"  - {node}")
    print("Workflows:")
    for wf in templates_available("workflow"):
        print(f"  - {wf}")

    print("\n=== Your Library ===")
    print("Nodes:")
    for node in library_items("node"):
        print(f"  - {node}")
    print("Workflows:")
    for wf in library_items("workflow"):
        print(f"  - {wf}")

def run_workflow(name: str, text: str, target_lang: str = None, recipient: str = None):
    module_name = f"agents_library.workflows.{name}"
    try:
        mod = importlib.import_module(module_name)
    except Exception as e:
        print(f"❌ Could not import workflow '{name}': {e}")
        return

    builder = getattr(mod, "build_workflow", None)
    if builder is None:
        print(f"❌ Workflow module {module_name} does not expose build_workflow()")
        return

    app = builder()
    inputs = {"text": text}
    if target_lang:
        inputs["target_lang"] = target_lang
    if recipient:
        inputs["recipient"] = recipient

    print(f"🚀 Running workflow: {name}")
    for step in app.stream(inputs):
        print("Step Output:", step)
    print("✅ Done")

def main(argv: List[str] = None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    parser_add = sub.add_parser("add")
    parser_add.add_argument("kind", choices=["node", "workflow"])
    parser_add.add_argument("name", help="name of template (without .py)")

    parser_list = sub.add_parser("list")


    parser_run = sub.add_parser("run")
    parser_run.add_argument("kind", choices=["workflow"])
    parser_run.add_argument("name")
    parser_run.add_argument("--text", required=True)
    parser_run.add_argument("--target_lang", default=None)
    parser_run.add_argument("--recipient", default=None, help="recipient email (optional)")

    # Add playground command
    parser_playground = sub.add_parser("playground", help="Run the interactive playground app.")

    args = parser.parse_args(argv)

    if args.cmd == "add":
        add_component(args.kind, args.name)
    elif args.cmd == "list":
        list_all()
    elif args.cmd == "run":
        run_workflow(args.name, args.text, args.target_lang, args.recipient)
    elif args.cmd == "playground":
        # Launch the Streamlit playground app
        os.system("streamlit run playground.py")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()