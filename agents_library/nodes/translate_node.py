# templates/nodes/translate_node.py
def translate_node(state: dict) -> dict:
    text = state.get("text", "")
    target_lang = state.get("target_lang", "es")
    translation = f"[{target_lang.upper()}] {text}" if text else ""
    new_state = state.copy()
    new_state["translation"] = translation
    return new_state