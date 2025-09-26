# templates/nodes/translate_node.py
from typing import Dict
from deep_translator import GoogleTranslator

def translate_node(state: Dict) -> Dict:
    """A node that translates text to a target language using Google Translate."""
    text = state.get("text", "")
    target_lang = state.get("target_lang", "es")
    
    if not text.strip():
        print("⚠️ No text content found for translation")
        new_state = state.copy()
        new_state["translation"] = ""
        return new_state
    
    try:
        print(f"🌐 Translating text to {target_lang}...")
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text)
        
        new_state = state.copy()
        new_state["translation"] = translated_text
        new_state["target_language"] = target_lang
        new_state["source_language"] = "auto-detected"
        
        print(f"✅ Translation completed to {target_lang}")
        return new_state
        
    except Exception as e:
        error_msg = f"Translation failed: {e}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["translation"] = f"Translation failed: {e}"
        new_state["target_language"] = target_lang
        return new_state