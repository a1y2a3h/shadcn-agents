# ===== Fixed templates/nodes/search_node.py =====
from typing import Dict
import requests
from bs4 import BeautifulSoup
import time

def search_node(state: Dict) -> Dict:
    """
    Web scraper node that extracts text content from URLs.
    Enhanced with better error handling and retry logic.
    """
    url = state.get("url", "").strip()
    if not url:
        error_msg = "No URL provided"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        new_state["error"] = error_msg
        return new_state
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        print(f"🔍 Scraping URL: {url}")
        
        # Add retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Attempt {attempt + 1} failed, retrying in 2 seconds...")
                    time.sleep(2)
                    continue
                else:
                    raise e
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside", "advertisement"]):
            element.decompose()
        
        # Extract text content
        text_content = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Remove excessive whitespace
        import re
        text_content = re.sub(r'\n\s*\n', '\n\n', text_content)
        text_content = text_content.strip()
        
        # Validate content
        if not text_content or len(text_content.strip()) < 50:
            error_msg = f"Insufficient content extracted from {url}"
            print(f"⚠️ {error_msg}")
            new_state = state.copy()
            new_state["text"] = f"Warning: {error_msg}"
            new_state["warning"] = error_msg
            return new_state
        
        # Limit text length to avoid overwhelming subsequent nodes
        max_length = 8000
        if len(text_content) > max_length:
            text_content = text_content[:max_length] + "\n...(content truncated)"
        
        new_state = state.copy()
        new_state["text"] = text_content
        new_state["scraped_url"] = url
        new_state["content_length"] = len(text_content)
        new_state["scrape_success"] = True
        
        print(f"✅ Successfully scraped {len(text_content)} characters from {url}")
        return new_state
        
    except requests.exceptions.Timeout:
        error_msg = f"Timeout while scraping {url}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        new_state["error"] = error_msg
        return new_state
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed for {url}: {str(e)[:100]}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: Could not scrape content from {url}"
        new_state["error"] = error_msg
        return new_state
    except Exception as e:
        error_msg = f"Unexpected error during scraping: {str(e)[:100]}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        new_state["error"] = error_msg
        return new_state