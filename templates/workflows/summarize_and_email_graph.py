# templates/workflows/summarize_and_email_graph.py
from langgraph.graph import StateGraph, END
from .nodes.search_node import search_node # <-- Changed to relative import
from .nodes.summarizer_node import summarizer_node # <-- Changed to relative import
from .nodes.email_node import email_node # <-- Changed to relative import

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