# templates/nodes/translate_node.py
from typing import Dict
from deep_translator import GoogleTranslator

def translate_node(state: Dict) -> Dict:
    """A node that translates text to a target language."""
    text = state.get("text", "")
    target_lang = state.get("target_lang", "es")
    
    if not text:
        return {"translation": ""}
    
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        new_state = state.copy()
        new_state["translation"] = translated_text
        return new_state
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        new_state = state.copy()
        new_state["translation"] = "Translation failed."
        return new_state