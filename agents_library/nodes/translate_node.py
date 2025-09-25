# templates/nodes/translate_node.py
from deep_translator import GoogleTranslator

def translate_node(state: dict) -> dict:
    """
    Translates text to the target language using Deep Translator (Google Translate backend).
    """
    text = state.get("text", "")
    target_lang = state.get("target_lang", "es")
    translation = ""
    if text:
        try:
            translation = GoogleTranslator(target=target_lang).translate(text)
        except Exception as e:
            translation = f"Translation error: {e}"
    new_state = state.copy()
    new_state["translation"] = translation
    return new_state