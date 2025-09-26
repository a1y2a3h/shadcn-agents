# main.py
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import importlib
import importlib.util
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

def setup_library_path(library_folder: str) -> bool:
    """Setup the library path for imports"""
    lib_path = Path(library_folder)
    if lib_path.exists():
        parent_path = lib_path.parent.absolute()
        if str(parent_path) not in sys.path:
            sys.path.insert(0, str(parent_path))
        return True
    return False

def safe_import_workflow(workflow_name: str, library_folder: str) -> Optional[callable]:
    """Import workflow with better error handling using importlib.util"""
    lib_path = Path(library_folder)
    workflow_file = lib_path / "workflows" / f"{workflow_name}.py"
    
    if not workflow_file.exists():
        print(f"❌ Workflow file not found: {workflow_file}")
        return None
    
    module_name = f"{library_folder}.workflows.{workflow_name}"
    
    try:
        # Use importlib.util for more robust importing
        spec = importlib.util.spec_from_file_location(module_name, workflow_file)
        
        if spec is None or spec.loader is None:
            print(f"❌ Could not create module spec for {workflow_name}")
            return None
        
        # Clear module cache to ensure fresh import
        if module_name in sys.modules:
            del sys.modules[module_name]
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        build_workflow = getattr(module, "build_workflow", None)
        
        if build_workflow is None:
            print(f"❌ Workflow '{workflow_name}' does not expose 'build_workflow' function")
            return None
            
        return build_workflow
        
    except ImportError as e:
        print(f"❌ Import error for workflow '{workflow_name}': {e}")
        print(f"💡 Make sure to add the workflow: shadcn-agent add workflow {workflow_name} --dest {library_folder}")
        return None
    except Exception as e:
        print(f"❌ Could not import workflow '{workflow_name}' from '{library_folder}': {e}")
        return None

def get_email_config() -> Dict[str, Optional[str]]:
    """Get email configuration from environment or user input"""
    recipient = os.getenv("DEFAULT_RECIPIENT")
    
    if not recipient:
        # Try to get from command line arguments
        if len(sys.argv) > 2:
            recipient = sys.argv[2]
        else:
            recipient = "test@example.com"  # Default fallback
            print(f"⚠️ No recipient email specified, using fallback: {recipient}")
            print("💡 Set DEFAULT_RECIPIENT in .env or pass as second argument")
    
    return {
        "sender_email": os.getenv("SENDER_EMAIL"),
        "sender_password": os.getenv("SENDER_PASSWORD"),
        "recipient": recipient
    }

def run_workflow_safely(workflow_name: str, workflow_builder: callable, inputs: Dict[str, Any]) -> bool:
    """Run a workflow with comprehensive error handling"""
    try:
        print(f"🚀 Running {workflow_name.replace('_', ' ').title()} Workflow...")
        app = workflow_builder()
        print("📥 Input:", inputs)
        
        step_count = 0
        for step in app.stream(inputs):
            step_count += 1
            print(f"📊 Step {step_count} Output:", step)
        
        print(f"✅ {workflow_name} completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print(f"\n⚠️ {workflow_name} interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Error running {workflow_name}: {e}")
        import traceback
        if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
            traceback.print_exc()
        return False

def main() -> int:
    """Main function with improved error handling and configuration"""
    
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

    # Get email configuration
    email_config = get_email_config()
    
    if not email_config["sender_email"] or not email_config["sender_password"]:
        print("⚠️ Email credentials not configured in .env file")
        print("💡 Workflows will run but email sending may fail")

    # Import workflows
    print("📦 Loading available workflows...")
    
    workflows_to_test = [
        ("summarize_and_email_graph", {
            "url": "https://en.wikipedia.org/wiki/Large_language_model",
            "recipient": email_config["recipient"]
        }),
        ("translate_and_email_graph", {
            "text": "LangGraph makes AI workflows modular and reusable.",
            "target_lang": "fr",
            "recipient": email_config["recipient"]
        }),
        ("scrape_and_summarize_graph", {
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
        })
    ]
    
    successful_runs = 0
    total_workflows = len(workflows_to_test)
    
    for workflow_name, test_inputs in workflows_to_test:
        build_workflow = safe_import_workflow(workflow_name, LIBRARY_FOLDER)
        
        if build_workflow:
            if run_workflow_safely(workflow_name, build_workflow, test_inputs):
                successful_runs += 1
            print()  # Add spacing between workflows
        else:
            print(f"⚠️ Could not run {workflow_name} from '{LIBRARY_FOLDER}'.")
            print(f"💡 Add it with: shadcn-agent add workflow {workflow_name} --dest {LIBRARY_FOLDER}")
            print()

    # Summary
    print("=" * 50)
    print(f"📊 Summary: {successful_runs}/{total_workflows} workflows completed successfully")
    
    if successful_runs == total_workflows:
        print("🎉 All workflows completed successfully!")
        return 0
    elif successful_runs > 0:
        print("⚠️ Some workflows completed with issues")
        return 0
    else:
        print("❌ No workflows could be completed")
        print("💡 Check your component setup and try again")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        if os.getenv("DEBUG", "").lower() in ("true", "1", "yes"):
            import traceback
            traceback.print_exc()
        sys.exit(1)