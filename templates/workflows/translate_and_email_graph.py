# ===== templates/workflows/translate_and_email_graph.py =====
from langgraph.graph import StateGraph, END

# Import nodes - these will be resolved when the template is copied to the user's project
try:
    from components.nodes.translate_node import translate_node
    from components.nodes.email_node import email_node
except ImportError:
    # Fallback for development/testing
    try:
        from ..nodes.translate_node import translate_node
        from ..nodes.email_node import email_node
    except ImportError as e:
        raise ImportError(f"Could not import required nodes. Make sure they are added to your project: {e}")

def build_workflow():
    """Build the translate and email workflow."""
    workflow = StateGraph(dict)
    workflow.add_node("translate", translate_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("translate")
    workflow.add_edge("translate", "email")
    workflow.add_edge("email", END)

    return workflow.compile()