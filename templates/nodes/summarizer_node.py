# templates/nodes/summarizer_node.py
from typing import Dict

def summarizer_node(state: Dict) -> Dict:
    """
    Simple text summarizer that takes the first portion of text.
    In production, you might want to integrate with an LLM for better summarization.
    """
    text = state.get("text", "")
    
    if not text.strip():
        print("⚠️ No text content found for summarization")
        new_state = state.copy()
        new_state["summary"] = "No content to summarize"
        return new_state
    
    # Simple word-based summarization
    words = text.split()
    summary_length = min(50, len(words))  # Take first 50 words or all if less
    summary = " ".join(words[:summary_length])
    
    if len(words) > summary_length:
        summary += "..."
    
    new_state = state.copy()
    new_state["summary"] = summary
    new_state["original_word_count"] = len(words)
    new_state["summary_word_count"] = summary_length
    
    print(f"📝 Summarized {len(words)} words down to {summary_length} words")
    return new_state