# ===== templates/workflows/summarize_and_email_graph.py =====
from langgraph.graph import StateGraph, END
from ..nodes.search_node import search_node
from ..nodes.summarizer_node import summarizer_node
from ..nodes.email_node import email_node

def build_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", "email")
    workflow.add_edge("email", END)

    return workflow.compile()