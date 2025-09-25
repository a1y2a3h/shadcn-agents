# templates/workflows/translate_and_email_graph.py
from langgraph.graph import StateGraph, END
from .nodes.translate_node import translate_node # <-- Changed to relative import
from .nodes.email_node import email_node # <-- Changed to relative import

def build_workflow():
    workflow = StateGraph(dict)

    workflow.add_node("translate", translate_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("translate")
    workflow.add_edge("translate", "email")
    workflow.add_edge("email", END)

    return workflow.compile()