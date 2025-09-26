# ===== Fixed templates/nodes/translate_node.py =====
from typing import Dict

def translate_node(state: Dict) -> Dict:
    """
    Enhanced translation node with better error handling and language detection.
    """
    text = state.get("text", "").strip()
    target_lang = state.get("target_lang", "es").lower().strip()
    
    if not text:
        print("⚠️ No text content found for translation")
        new_state = state.copy()
        new_state["translation"] = ""
        new_state["translation_status"] = "no_input"
        return new_state
    
    # Validate target language
    common_languages = {
        'es': 'Spanish', 'fr': 'French', 'de': 'German', 'it': 'Italian',
        'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese', 'ko': 'Korean',
        'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi', 'nl': 'Dutch'
    }
    
    if len(target_lang) != 2 or target_lang not in common_languages:
        print(f"⚠️ Unusual target language code: {target_lang}")
    
    try:
        print(f"🌐 Translating text to {target_lang}...")
        
        # Import here to handle missing dependency gracefully
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            error_msg = "deep-translator library not found. Install with: pip install deep-translator"
            print(f"❌ {error_msg}")
            new_state = state.copy()
            new_state["translation"] = f"Translation unavailable: {error_msg}"
            new_state["translation_status"] = "dependency_missing"
            new_state["error"] = error_msg
            return new_state
        
        # Limit text length for translation API
        max_length = 1000
        text_to_translate = text[:max_length] if len(text) > max_length else text
        
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text_to_translate)
        
        if not translated_text or translated_text == text_to_translate:
            print("⚠️ Translation returned empty or unchanged text")
            new_state = state.copy()
            new_state["translation"] = text_to_translate
            new_state["translation_status"] = "unchanged"
            new_state["target_language"] = target_lang
            return new_state
        
        new_state = state.copy()
        new_state["translation"] = translated_text
        new_state["target_language"] = target_lang
        new_state["target_language_name"] = common_languages.get(target_lang, target_lang)
        new_state["source_language"] = "auto-detected"
        new_state["translation_status"] = "success"
        new_state["translation_length"] = len(translated_text)
        
        if len(text) > max_length:
            new_state["translation_note"] = f"Original text truncated from {len(text)} to {max_length} characters"
        
        print(f"✅ Translation completed to {target_lang}")
        return new_state
        
    except Exception as e:
        error_msg = f"Translation failed: {str(e)[:200]}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["translation"] = f"Translation failed: {str(e)}"
        new_state["target_language"] = target_lang
        new_state["translation_status"] = "error"
        new_state["error"] = error_msg
        return new_state