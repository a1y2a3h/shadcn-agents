# templates/nodes/search_node.py
from typing import Dict
import requests
from bs4 import BeautifulSoup

def search_node(state: Dict) -> Dict:
    """
    Web scraper node that extracts text content from URLs.
    """
    url = state.get("url", "")
    if not url:
        error_msg = "No URL provided"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        return new_state
    
    # Add a User-Agent header to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print(f"🔍 Scraping URL: {url}")
        # Pass the headers with the request
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text_content = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to avoid overwhelming subsequent nodes
        max_length = 8000
        if len(text_content) > max_length:
            text_content = text_content[:max_length] + "\n...(content truncated)"
        
        new_state = state.copy()
        new_state["text"] = text_content
        new_state["scraped_url"] = url
        print(f"✅ Successfully scraped {len(text_content)} characters from {url}")
        return new_state
        
    except requests.exceptions.Timeout:
        error_msg = f"Timeout while scraping {url}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        return new_state
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed for {url}: {e}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: Could not scrape content from {url}"
        return new_state
    except Exception as e:
        error_msg = f"Unexpected error during scraping: {e}"
        print(f"❌ {error_msg}")
        new_state = state.copy()
        new_state["text"] = f"Error: {error_msg}"
        return new_state