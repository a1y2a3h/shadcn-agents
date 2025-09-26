# ===== Fixed templates/workflows/translate_and_email_graph.py =====
from langgraph.graph import StateGraph, END
from typing import Dict

def build_workflow():
    """Build the translate and email workflow."""
    
    # Import nodes with better error handling
    try:
        from components.nodes.translate_node import translate_node
        from components.nodes.email_node import email_node
    except ImportError as e:
        raise ImportError(
            f"Could not import required nodes: {e}\n"
            f"Make sure to add the required components:\n"
            f"  shadcn-agent add node translate_node\n"
            f"  shadcn-agent add node email_node"
        )

    workflow = StateGraph(dict)
    workflow.add_node("translate", translate_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("translate")
    workflow.add_edge("translate", "email")
    workflow.add_edge("email", END)

    return workflow.compile()

