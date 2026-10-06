import re
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """
    Cleans text by removing HTML tags, normalizing whitespace, and removing noise.
    """
    if not text:
        return ""
    
    # Remove HTML tags if any slipped through
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    
    # Normalize whitespace (remove extra spaces, tabs, newlines)
    text = re.sub(r'\s+', ' ', text)
    
    # Basic noise removal (e.g., removing non-ascii or very weird characters could happen here)
    # Keeping it simple and readable
    text = text.strip()
    
    return text
