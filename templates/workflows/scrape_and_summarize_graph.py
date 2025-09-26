# ===== templates/workflows/scrape_and_summarize_graph.py =====
from langgraph.graph import StateGraph, END

# Import nodes - these will be resolved when the template is copied to the user's project
try:
    from components.nodes.search_node import search_node
    from components.nodes.summarizer_node import summarizer_node
except ImportError:
    # Fallback for development/testing
    try:
        from ..nodes.search_node import search_node
        from ..nodes.summarizer_node import summarizer_node
    except ImportError as e:
        raise ImportError(f"Could not import required nodes. Make sure they are added to your project: {e}")

def build_workflow():
    """Build the scrape and summarize workflow."""
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", END)

    return workflow.compile()