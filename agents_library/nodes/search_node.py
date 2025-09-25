# templates/nodes/search_node.py
from typing import Dict
import requests
from bs4 import BeautifulSoup

def search_node(state: Dict) -> Dict:
    url = state.get("url", "")
    if not url:
        return {"text": "Error: No URL provided."}
    
    # Add a User-Agent header to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Pass the headers with the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        
        new_state = state.copy()
        new_state["text"] = text_content[:5000]
        return new_state
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return {"text": f"Error: Could not scrape content from {url}."}