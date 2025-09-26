# ===== Fixed templates/workflows/scrape_and_summarize_graph.py =====
from langgraph.graph import StateGraph, END
from typing import Dict

def build_workflow():
    """Build the scrape and summarize workflow."""
    
    # Import nodes with better error handling
    try:
        from components.nodes.search_node import search_node
        from components.nodes.summarizer_node import summarizer_node
    except ImportError as e:
        raise ImportError(
            f"Could not import required nodes: {e}\n"
            f"Make sure to add the required components:\n"
            f"  shadcn-agent add node search_node\n"
            f"  shadcn-agent add node summarizer_node"
        )

    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", END)

    return workflow.compile()