#!/usr/bin/python3
"""
Oil Price Scraper

This script scrapes the current oil price from Patriot Discount Oil's website
and outputs the price along with the current date.

Dependencies:
    - beautifulsoup4
    - requests
"""

import logging
from datetime import datetime
from typing import Optional, Tuple

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_webpage_content(url: str) -> Optional[str]:
    """
    Fetches content from the specified URL.
    
    Args:
        url: The URL to fetch content from
        
    Returns:
        The webpage content as string if successful, None otherwise
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logger.error(f"Failed to fetch webpage: {e}")
        return None

def extract_oil_price(html_content: str) -> Optional[Tuple[float, datetime]]:
    """
    Extracts the oil price from the HTML content.
    
    Args:
        html_content: Raw HTML content to parse
        
    Returns:
        Tuple of (price, timestamp) if found, None otherwise
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        search_text = "Today's Oil Price"
        
        # Using the original approach that works
        found_item = soup.find(lambda tag: tag.name == "div" and search_text in tag.text)
        if not found_item:
            logger.warning("Price information not found in webpage")
            return None
            
        # Similar to original code, but with better error handling
        import re
        price_matches = re.findall(r"[0-9.]+", found_item.text)
        if not price_matches:
            logger.warning("Could not parse price from text")
            return None
            
        price = float(price_matches[0])
        timestamp = datetime.now()
        
        return price, timestamp
        
    except Exception as e:
        logger.error(f"Error parsing HTML content: {e}")
        return None

def main():
    """Main function to run the oil price scraper."""
    URL = "https://patriotdiscountoil.com/"
    
    # Fetch webpage content
    content = get_webpage_content(URL)
    if not content:
        return
    
    # Extract price and timestamp
    result = extract_oil_price(content)
    if not result:
        return
    
    price, timestamp = result
    
    # Output result in same format as original script
    print(f'Date: {timestamp:%Y%m%d}, PDO Price: {price}')

if __name__ == "__main__":
    main()
