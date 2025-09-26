# main.py
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import importlib

# Load environment variables from .env file
load_dotenv()

def setup_library_path(library_folder):
    """Setup the library path for imports"""
    lib_path = Path(library_folder)
    if lib_path.exists():
        parent_path = lib_path.parent.absolute()
        if str(parent_path) not in sys.path:
            sys.path.insert(0, str(parent_path))
        return True
    return False

def import_workflow(workflow_name, library_folder):
    """Import workflow with better error handling"""
    module_name = f"{library_folder}.workflows.{workflow_name}"
    try:
        # Clear module cache to ensure fresh import
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        mod = importlib.import_module(module_name)
        return getattr(mod, "build_workflow", None)
    except ImportError as e:
        print(f"❌ Import error for workflow '{workflow_name}': {e}")
        print(f"💡 Make sure to add the workflow: shadcn-agent add workflow {workflow_name} --dest {library_folder}")
        return None
    except Exception as e:
        print(f"❌ Could not import workflow '{workflow_name}' from '{library_folder}': {e}")
        return None

def main():
    # Allow user to specify the library folder via env var or command-line arg
    LIBRARY_FOLDER = os.environ.get("AGENTS_LIBRARY", "components")
    if len(sys.argv) > 1:
        LIBRARY_FOLDER = sys.argv[1]

    print(f"🔧 Using library folder: {LIBRARY_FOLDER}")

    # Setup library path
    if not setup_library_path(LIBRARY_FOLDER):
        print(f"❌ Library folder '{LIBRARY_FOLDER}' not found!")
        print(f"💡 Initialize it with: shadcn-agent init --dest {LIBRARY_FOLDER}")
        return 1

    # Import workflows
    build_summary_workflow = import_workflow("summarize_and_email_graph", LIBRARY_FOLDER)
    build_translate_workflow = import_workflow("translate_and_email_graph", LIBRARY_FOLDER)

    # Run workflows if available
    if build_summary_workflow:
        print(f"🚀 Running Summarize + Email Workflow from '{LIBRARY_FOLDER}'...")
        try:
            app1 = build_summary_workflow()
            summarize_input = {
                "url": "https://en.wikipedia.org/wiki/Large_language_model",
                "recipient": "aryanbagale786@gmail.com"  # Change this to your email
            }
            print("📥 Input:", summarize_input)
            step_count = 0
            for step in app1.stream(summarize_input):
                step_count += 1
                print(f"📊 Step {step_count} Output:", step)
        except Exception as e:
            print(f"❌ Error running summarize workflow: {e}")
    else:
        print(f"⚠️ Could not run summarize_and_email_graph from '{LIBRARY_FOLDER}'.")

    if build_translate_workflow:
        print(f"\n🚀 Running Translate + Email Workflow from '{LIBRARY_FOLDER}'...")
        try:
            app2 = build_translate_workflow()
            translate_input = {
                "text": "LangGraph makes AI workflows modular and reusable.",
                "target_lang": "fr",
                "recipient": "aryanbagale786@gmail.com"  # Change this to your email
            }
            print("📥 Input:", translate_input)
            step_count = 0
            for step in app2.stream(translate_input):
                step_count += 1
                print(f"📊 Step {step_count} Output:", step)
        except Exception as e:
            print(f"❌ Error running translate workflow: {e}")
    else:
        print(f"⚠️ Could not run translate_and_email_graph from '{LIBRARY_FOLDER}'.")

    print("\n✅ All workflows completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())