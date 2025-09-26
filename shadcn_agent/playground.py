import streamlit as st
import os
import sys
from pathlib import Path
import importlib

# Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Sidebar for library folder selection
default_lib = os.environ.get("SHADCN_AGENT_LIB", "components")
lib_folder = st.sidebar.text_input("Library Folder", default_lib)

# Add current working directory to Python path for importing user's components
cwd = Path.cwd()
if str(cwd) not in sys.path:
    sys.path.insert(0, str(cwd))

def import_workflow(workflow_name):
    module_name = f"{lib_folder}.workflows.{workflow_name}"
    try:
        # Force reload in case user modified the workflow
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        mod = importlib.import_module(module_name)
        return getattr(mod, "build_workflow", None)
    except Exception as e:
        st.warning(f"Could not import workflow '{workflow_name}' from '{lib_folder}': {e}")
        return None

def import_node(node_name):
    module_name = f"{lib_folder}.nodes.{node_name}"
    try:
        # Force reload in case user modified the node
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        mod = importlib.import_module(module_name)
        return getattr(mod, node_name, None)
    except Exception as e:
        st.warning(f"Could not import node '{node_name}' from '{lib_folder}': {e}")
        return None

def check_library_exists():
    """Check if the library folder exists"""
    lib_path = Path(lib_folder)
    if not lib_path.exists():
        st.error(f"📁 Library folder '{lib_folder}' not found!")
        st.info(f"💡 Initialize it first: `shadcn-agent init --dest {lib_folder}`")
        return False
    return True

def main():
    st.title("🤖 shadcn-agent Playground")
    st.markdown("*Test your AI workflows in an interactive environment*")
    
    if not check_library_exists():
        return
    
    # Import workflows dynamically
    build_summary_workflow = import_workflow("summarize_and_email_graph")
    build_translate_workflow = import_workflow("translate_and_email_graph")
    build_scrape_summarize_workflow = import_workflow("scrape_and_summarize_graph")
    
    # Workflow selection
    workflow_options = [
        "Summarize + Email", 
        "Translate + Email", 
        "Scrape + Summarize", 
        "Custom Workflow Builder"
    ]
    
    workflow = st.selectbox("Choose a workflow", workflow_options)
    
    if workflow == "Summarize + Email":
        st.markdown("### 🔗 Summarize + Email Workflow")
        st.markdown("Scrapes a URL → Summarizes content → Sends email")
        
        url = st.text_input("URL to summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
        recipient = st.text_input("Recipient Email", "test@example.com")
        
        if st.button("🚀 Run Workflow", type="primary"):
            if build_summary_workflow:
                with st.spinner("Running workflow..."):
                    try:
                        app = build_summary_workflow()
                        summarize_input = {"url": url, "recipient": recipient}
                        st.write("## 📊 Workflow Output:")
                        results = []
                        for step in app.stream(summarize_input):
                            st.json(step)
                            results.append(step)
                        st.download_button(
                            "💾 Download Results as JSON", 
                            data=str(results), 
                            file_name="summarize_results.json",
                            mime="application/json"
                        )
                        st.success("✅ Workflow completed!")
                    except Exception as e:
                        st.error(f"❌ Workflow failed: {e}")
            else:
                st.error(f"Workflow not available in '{lib_folder}'. Add it first:")
                st.code(f"shadcn-agent add workflow summarize_and_email_graph --dest {lib_folder}")
    
    elif workflow == "Translate + Email":
        st.markdown("### 🌐 Translate + Email Workflow")
        st.markdown("Translates text → Sends email")
        
        text = st.text_area("Text to translate", "Hello, how are you?")
        target_lang = st.text_input("Target Language (e.g., fr, es, de)", "fr")
        recipient = st.text_input("Recipient Email", "test@example.com")
        
        if st.button("🚀 Run Workflow", type="primary"):
            if build_translate_workflow:
                with st.spinner("Running workflow..."):
                    try:
                        app = build_translate_workflow()
                        translate_input = {"text": text, "target_lang": target_lang, "recipient": recipient}
                        st.write("## 📊 Workflow Output:")
                        results = []
                        for step in app.stream(translate_input):
                            st.json(step)
                            results.append(step)
                        st.download_button(
                            "💾 Download Results as JSON", 
                            data=str(results), 
                            file_name="translate_results.json",
                            mime="application/json"
                        )
                        st.success("✅ Workflow completed!")
                    except Exception as e:
                        st.error(f"❌ Workflow failed: {e}")
            else:
                st.error(f"Workflow not available in '{lib_folder}'. Add it first:")
                st.code(f"shadcn-agent add workflow translate_and_email_graph --dest {lib_folder}")
    
    elif workflow == "Scrape + Summarize":
        st.markdown("### 🔍 Scrape + Summarize Workflow")
        st.markdown("Scrapes a URL → Summarizes content")
        
        url = st.text_input("URL to scrape and summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
        
        if st.button("🚀 Run Workflow", type="primary"):
            if build_scrape_summarize_workflow:
                with st.spinner("Running workflow..."):
                    try:
                        app = build_scrape_summarize_workflow()
                        scrape_input = {"url": url}
                        st.write("## 📊 Workflow Output:")
                        results = []
                        for step in app.stream(scrape_input):
                            st.json(step)
                            results.append(step)
                        st.download_button(
                            "💾 Download Results as JSON", 
                            data=str(results), 
                            file_name="scrape_results.json",
                            mime="application/json"
                        )
                        st.success("✅ Workflow completed!")
                    except Exception as e:
                        st.error(f"❌ Workflow failed: {e}")
            else:
                st.error(f"Workflow not available in '{lib_folder}'. Add it first:")
                st.code(f"shadcn-agent add workflow scrape_and_summarize_graph --dest {lib_folder}")
    
    elif workflow == "Custom Workflow Builder":
        st.markdown("### 🛠️ Custom Workflow Builder")
        st.info("Select nodes and chain them to build your own workflow.")
        
        # Available nodes
        node_options = {
            "search_node": ("Search (Web Scraper)", "url"),
            "summarizer_node": ("Summarizer", "text"),
            "translate_node": ("Translator", "text"),
            "email_node": ("Email Sender", "body")
        }
        
        node_names = list(node_options.keys())
        
        selected_nodes = st.multiselect(
            "Select nodes to include (order matters):",
            options=node_names,
            format_func=lambda n: node_options[n][0],
            default=["search_node", "summarizer_node"]
        )
        
        # Input fields for the first node
        user_inputs = {}
        if selected_nodes:
            first_node = selected_nodes[0]
            st.markdown(f"### Input for {node_options[first_node][0]}")
            
            if first_node == "search_node":
                user_inputs["url"] = st.text_input("URL", "https://en.wikipedia.org/wiki/Artificial_intelligence")
            elif first_node == "summarizer_node" or first_node == "translate_node":
                user_inputs["text"] = st.text_area("Text", "Hello, world!")
                if first_node == "translate_node":
                    user_inputs["target_lang"] = st.text_input("Target Language", "fr")
            elif first_node == "email_node":
                user_inputs["body"] = st.text_area("Email Body", "This is a test email.")
                user_inputs["recipient"] = st.text_input("Recipient Email", "test@example.com")
        
        if st.button("🚀 Run Custom Workflow", type="primary") and selected_nodes:
            # Dynamically import node functions from selected library folder
            node_funcs = {}
            missing_nodes = []
            
            for node in selected_nodes:
                func = import_node(node)
                if func is None:
                    missing_nodes.append(node)
                else:
                    node_funcs[node] = func
            
            if missing_nodes:
                st.error(f"Missing nodes: {', '.join(missing_nodes)}")
                for node in missing_nodes:
                    st.code(f"shadcn-agent add node {node} --dest {lib_folder}")
                return
            
            with st.spinner("Running custom workflow..."):
                try:
                    state = user_inputs.copy()
                    results = []
                    
                    st.write("## 📊 Custom Workflow Output:")
                    for i, node in enumerate(selected_nodes):
                        func = node_funcs[node]
                        state = func(state)
                        
                        step_result = {f"Step {i+1} - {node_options[node][0]}": state}
                        st.json(step_result)
                        results.append(step_result)
                    
                    st.download_button(
                        "💾 Download Results as JSON", 
                        data=str(results), 
                        file_name="custom_workflow_results.json",
                        mime="application/json"
                    )
                    st.success("✅ Custom workflow completed!")
                except Exception as e:
                    st.error(f"❌ Custom workflow failed: {e}")
    
    # Sidebar info
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📚 Quick Setup")
        st.code(f"""
# Initialize project
shadcn-agent init --dest {lib_folder}

# Add components  
shadcn-agent add node search_node --dest {lib_folder}
shadcn-agent add workflow scrape_and_summarize_graph --dest {lib_folder}
        """)
        
        st.markdown("### 🔧 Environment Setup")
        st.markdown("Create `.env` file:")
        st.code("""
SENDER_EMAIL=your@email.com
SENDER_PASSWORD=your_app_password
        """)

if __name__ == "__main__":
    main()