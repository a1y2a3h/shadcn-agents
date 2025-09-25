# main.py
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The rest of your code
sys.path.append('.')

from agents_library.workflows.summarize_and_email_graph import build_workflow as build_summary_workflow
from agents_library.workflows.translate_and_email_graph import build_workflow as build_translate_workflow

if __name__ == "__main__":
    print("🚀 Running Summarize + Email Workflow...")
    app1 = build_summary_workflow()
    summarize_input = {
        "url": "https://en.wikipedia.org/wiki/Large_language_model",
        "recipient": "aryanbagale786@gmail.com" # Change this to your email
    }
    for step in app1.stream(summarize_input):
        print("Step Output:", step)

    print("\n🚀 Running Translate + Email Workflow...")
    app2 = build_translate_workflow()
    translate_input = {
        "text": "LangGraph makes AI workflows modular and reusable.",
        "target_lang": "fr",
        "recipient": "aryanbagale786@gmail.com" # Change this to your email
    }
    for step in app2.stream(translate_input):
        print("Step Output:", step)

    print("\n✅ All Workflows complete!")