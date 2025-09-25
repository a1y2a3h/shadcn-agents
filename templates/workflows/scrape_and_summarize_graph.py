# templates/workflows/scrape_and_summarize_graph.py
from langgraph.graph import StateGraph, END
from agents_library.nodes.search_node import search_node
from agents_library.nodes.summarizer_node import summarizer_node

def build_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("search", search_node)
    workflow.add_node("summarizer", summarizer_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "summarizer")
    workflow.add_edge("summarizer", END)

    return workflow.compile()
