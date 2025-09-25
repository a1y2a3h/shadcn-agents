# templates/nodes/summarizer_node.py
def summarizer_node(state: dict) -> dict:
    text = state.get("text", "")
    words = text.split()
    summary = " ".join(words[:30]) + ("..." if len(words) > 30 else "")
    new_state = state.copy()
    new_state["summary"] = summary
    return new_state