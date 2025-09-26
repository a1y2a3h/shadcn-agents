# ===== templates/workflows/summarize_and_email_graph.py =====
from langgraph.graph import StateGraph, END

# Import nodes - these will be resolved when the template is copied to the user's project
try:
    from components.nodes.search_node import search_node
    from components.nodes.summarizer_node import summarizer_node  
    from components.nodes.email_node import email_node
except ImportError:
    # Fallback for development/testing
    try:
        from ..nodes.search_node import search_node
        from ..nodes.summarizer_node import summarizer_node
        from ..nodes.email_node import email_node
    except ImportError as e:
        raise ImportError(f"Could not import required nodes. Make sure they are added to your project: {e}")

def build_workflow():
    """Build the summarize and email workflow."""
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", "email")
    workflow.add_edge("email", END)

    return workflow.compile()