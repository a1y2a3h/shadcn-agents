# ===== Fixed templates/workflows/summarize_and_email_graph.py =====
from langgraph.graph import StateGraph, END
from typing import Dict

def build_workflow():
    """Build the summarize and email workflow."""
    
    # Import nodes with better error handling
    try:
        from components.nodes.search_node import search_node
        from components.nodes.summarizer_node import summarizer_node  
        from components.nodes.email_node import email_node
    except ImportError as e:
        raise ImportError(
            f"Could not import required nodes: {e}\n"
            f"Make sure to add the required components:\n"
            f"  shadcn-agent add node search_node\n"
            f"  shadcn-agent add node summarizer_node\n"
            f"  shadcn-agent add node email_node"
        )
    
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", "email")
    workflow.add_edge("email", END)

    return workflow.compile()
