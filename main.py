# main.py
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The rest of your code
sys.path.append('.')


import importlib

# Allow user to specify the library folder via env var or command-line arg
LIBRARY_FOLDER = os.environ.get("AGENTS_LIBRARY", "agents_library")
if len(sys.argv) > 1:
    LIBRARY_FOLDER = sys.argv[1]

def import_workflow(workflow_name):
    module_name = f"{LIBRARY_FOLDER}.workflows.{workflow_name}"
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, "build_workflow", None)
    except Exception as e:
        print(f"❌ Could not import workflow '{workflow_name}' from '{LIBRARY_FOLDER}': {e}")
        return None

build_summary_workflow = import_workflow("summarize_and_email_graph")
build_translate_workflow = import_workflow("translate_and_email_graph")

if __name__ == "__main__":
    if build_summary_workflow:
        print(f"🚀 Running Summarize + Email Workflow from '{LIBRARY_FOLDER}'...")
        app1 = build_summary_workflow()
        summarize_input = {
            "url": "https://en.wikipedia.org/wiki/Large_language_model",
            "recipient": "aryanbagale786@gmail.com" # Change this to your email
        }
        for step in app1.stream(summarize_input):
            print("Step Output:", step)
    else:
        print(f"❌ Could not run summarize_and_email_graph from '{LIBRARY_FOLDER}'. Make sure it is scaffolded.")

    if build_translate_workflow:
        print(f"\n🚀 Running Translate + Email Workflow from '{LIBRARY_FOLDER}'...")
        app2 = build_translate_workflow()
        translate_input = {
            "text": "LangGraph makes AI workflows modular and reusable.",
            "target_lang": "fr",
            "recipient": "aryanbagale786@gmail.com" # Change this to your email
        }
        for step in app2.stream(translate_input):
            print("Step Output:", step)
    else:
        print(f"❌ Could not run translate_and_email_graph from '{LIBRARY_FOLDER}'. Make sure it is scaffolded.")

    print("\n✅ All Workflows complete!")