# templates/workflows/translate_and_email_graph.py
from langgraph.graph import StateGraph, END
from agents_library.nodes.translate_node import translate_node
from agents_library.nodes.email_node import email_node

def build_workflow():
    workflow = StateGraph(dict)

    workflow.add_node("translate", translate_node)
    workflow.add_node("email", email_node)

    workflow.set_entry_point("translate")
    workflow.add_edge("translate", "email")
    workflow.add_edge("email", END)

    return workflow.compile()