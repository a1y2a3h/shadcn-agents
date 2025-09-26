# ===== Fixed templates/nodes/summarizer_node.py =====
from typing import Dict
import re

def summarizer_node(state: Dict) -> Dict:
    """
    Enhanced text summarizer with better logic and error handling.
    Uses extractive summarization by selecting key sentences.
    """
    text = state.get("text", "").strip()
    
    if not text:
        print("⚠️ No text content found for summarization")
        new_state = state.copy()
        new_state["summary"] = "No content to summarize"
        new_state["summary_method"] = "none"
        return new_state
    
    # Clean the text
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    try:
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            print("⚠️ Could not extract meaningful sentences")
            new_state = state.copy()
            new_state["summary"] = text[:200] + "..." if len(text) > 200 else text
            new_state["summary_method"] = "truncation"
            return new_state
        
        # Determine summary length based on content size
        total_sentences = len(sentences)
        if total_sentences <= 3:
            summary_sentences = sentences
            method = "all_sentences"
        elif total_sentences <= 10:
            summary_sentences = sentences[:3]
            method = "first_sentences"
        else:
            # Take first, middle, and key sentences
            summary_sentences = [
                sentences[0],  # First sentence
                sentences[total_sentences // 2],  # Middle sentence
                sentences[-2] if len(sentences) > 1 else sentences[-1]  # Near-end sentence
            ]
            method = "extractive"
        
        summary = '. '.join(summary_sentences)
        if not summary.endswith('.'):
            summary += '.'
        
        # Ensure summary isn't too long
        max_summary_length = 500
        if len(summary) > max_summary_length:
            words = summary.split()
            truncated_words = words[:max_summary_length//7]  # Rough word estimate
            summary = ' '.join(truncated_words) + "..."
            method += "_truncated"
        
        word_count = len(text.split())
        summary_word_count = len(summary.split())
        
        new_state = state.copy()
        new_state["summary"] = summary
        new_state["original_word_count"] = word_count
        new_state["summary_word_count"] = summary_word_count
        new_state["summary_method"] = method
        new_state["compression_ratio"] = round(summary_word_count / word_count, 2) if word_count > 0 else 0
        
        print(f"📝 Summarized {word_count} words down to {summary_word_count} words using {method}")
        return new_state
        
    except Exception as e:
        error_msg = f"Summarization failed: {str(e)[:100]}"
        print(f"❌ {error_msg}")
        
        # Fallback to simple truncation
        words = text.split()
        fallback_length = min(50, len(words))
        fallback_summary = " ".join(words[:fallback_length])
        if len(words) > fallback_length:
            fallback_summary += "..."
        
        new_state = state.copy()
        new_state["summary"] = fallback_summary
        new_state["original_word_count"] = len(words)
        new_state["summary_word_count"] = fallback_length
        new_state["summary_method"] = "fallback_truncation"
        new_state["error"] = error_msg
        
        return new_state