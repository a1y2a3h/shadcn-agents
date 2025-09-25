
import streamlit as st
import os
from dotenv import load_dotenv

import importlib

# Sidebar for library folder selection
default_lib = os.environ.get("AGENTS_LIBRARY", "agents_library")
lib_folder = st.sidebar.text_input("Library Folder", default_lib)

def import_workflow(workflow_name):
    module_name = f"{lib_folder}.workflows.{workflow_name}"
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, "build_workflow", None)
    except Exception as e:
        st.warning(f"Could not import workflow '{workflow_name}' from '{lib_folder}': {e}")
        return None

def import_node(node_name):
    module_name = f"{lib_folder}.nodes.{node_name}"
    try:
        mod = importlib.import_module(module_name)
        return getattr(mod, node_name, None)
    except Exception as e:
        st.warning(f"Could not import node '{node_name}' from '{lib_folder}': {e}")
        return None

build_summary_workflow = import_workflow("summarize_and_email_graph")
build_translate_workflow = import_workflow("translate_and_email_graph")
build_scrape_summarize_workflow = import_workflow("scrape_and_summarize_graph")

load_dotenv()

st.title("shadcn-agent Playground")


workflow = st.selectbox("Choose a workflow", ["Summarize + Email", "Translate + Email", "Scrape + Summarize", "Custom Workflow Builder"])

if workflow == "Summarize + Email":
    url = st.text_input("URL to summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
    recipient = st.text_input("Recipient Email", "test@example.com")
    if st.button("Run Workflow"):
        if build_summary_workflow:
            app = build_summary_workflow()
            summarize_input = {"url": url, "recipient": recipient}
            st.write("## Workflow Output:")
            results = []
            for step in app.stream(summarize_input):
                st.json(step)
                results.append(step)
            st.download_button("Download Results as JSON", data=str(results), file_name="results.json")
        else:
            st.error(f"Workflow not available in '{lib_folder}'. Scaffold it first.")
elif workflow == "Translate + Email":
    text = st.text_area("Text to translate", "Hello, how are you?")
    target_lang = st.text_input("Target Language (e.g., fr, es, de)", "fr")
    recipient = st.text_input("Recipient Email", "test@example.com")
    if st.button("Run Workflow"):
        if build_translate_workflow:
            app = build_translate_workflow()
            translate_input = {"text": text, "target_lang": target_lang, "recipient": recipient}
            st.write("## Workflow Output:")
            results = []
            for step in app.stream(translate_input):
                st.json(step)
                results.append(step)
            st.download_button("Download Results as JSON", data=str(results), file_name="results.json")
        else:
            st.error(f"Workflow not available in '{lib_folder}'. Scaffold it first.")
elif workflow == "Scrape + Summarize":
    url = st.text_input("URL to scrape and summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
    if st.button("Run Workflow"):
        if build_scrape_summarize_workflow:
            app = build_scrape_summarize_workflow()
            scrape_input = {"url": url}
            st.write("## Workflow Output:")
            results = []
            for step in app.stream(scrape_input):
                st.json(step)
                results.append(step)
            st.download_button("Download Results as JSON", data=str(results), file_name="results.json")
        else:
            st.error(f"Workflow not available in '{lib_folder}'. Scaffold it first.")

elif workflow == "Custom Workflow Builder":
    st.write("### Custom Workflow Builder")
    st.info("Select nodes and order to build your own workflow.")

    # Available nodes
    node_options = {
        "search_node": ("Search (Web Scraper)", "url"),
        "summarizer_node": ("Summarizer", "text"),
        "translate_node": ("Translator", "text"),
        "email_node": ("Email Sender", "body")
    }

    node_names = list(node_options.keys())
    node_labels = [node_options[n][0] for n in node_names]

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
        if first_node == "search_node":
            user_inputs["url"] = st.text_input("URL", "https://en.wikipedia.org/wiki/Artificial_intelligence")
        elif first_node == "summarizer_node" or first_node == "translate_node":
            user_inputs["text"] = st.text_area("Text", "Hello, world!")
        elif first_node == "email_node":
            user_inputs["body"] = st.text_area("Email Body", "This is a test email.")
            user_inputs["recipient"] = st.text_input("Recipient Email", "test@example.com")

    if st.button("Run Custom Workflow") and selected_nodes:
        # Dynamically import node functions from selected library folder
        node_funcs = {}
        for node in selected_nodes:
            func = import_node(node)
            if func is None:
                st.error(f"Node '{node}' not available in '{lib_folder}'. Scaffold it first.")
                return
            node_funcs[node] = func
        state = user_inputs.copy()
        results = []
        for node in selected_nodes:
            func = node_funcs[node]
            state = func(state)
            st.json({node_options[node][0]: state})
            results.append({node_options[node][0]: state})
        st.download_button("Download Results as JSON", data=str(results), file_name="results.json")
