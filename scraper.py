"""
Web scraping functionality for extracting oil prices.
"""
import logging
import re
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup
from datetime import datetime

## import sys
## sys.path.append(".") # Adds higher directory to python modules path.


## from .config import TARGET_URL, PRICE_IDENTIFIER
from config import TARGET_URL, PRICE_IDENTIFIER

logger = logging.getLogger(__name__)

class ScraperError(Exception):
    """Exception raised for errors in the scraper module."""
    pass

def cursor__scrape_oil_price():
    """
    Scrape the oil price from the target website.
    
    Returns:
        Decimal: The extracted oil price as a Decimal
        
    Raises:
        ScraperError: If there are issues with the request or parsing
    """
    try:
        logger.info(f"Sending request to {TARGET_URL}")
        response = requests.get(TARGET_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve data from {TARGET_URL}: {e}")
        raise ScraperError(f"Network request failed: {e}")

    try:
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find the section containing "Today's Oil Price"
        price_elements = soup.find_all(text=lambda text: text and PRICE_IDENTIFIER in text)
        
        if not price_elements:
            logger.error(f"Could not find text containing '{PRICE_IDENTIFIER}'")
            raise ScraperError(f"Price identifier '{PRICE_IDENTIFIER}' not found on the page")
        
        # Get the parent element and search nearby for price
        for element in price_elements:
            parent = element.parent
            
            # Look in this element and its siblings for a price pattern
            price_pattern = r'\$\s*(\d+\.\d+)'
            
            # Check the parent and its siblings
            for sibling in list(parent.next_siblings) + [parent]:
                if sibling.text:
                    price_match = re.search(price_pattern, sibling.text)
                    if price_match:
                        price_str = price_match.group(1)
                        logger.info(f"Found price: ${price_str}")
                        return extract_and_validate_price(price_str)
                        # return Decimal(price_str)
            
            # If not found in siblings, check parent's parent
            if parent.parent:
                price_match = re.search(price_pattern, parent.parent.text)
                if price_match:
                    price_str = price_match.group(1)
                    logger.info(f"Found price: ${price_str}")
                    return extract_and_validate_price(price_str)
                    # return Decimal(price_str)
        
        # If we reach here, we couldn't find the price
        logger.error("Price pattern not found near the identifier")
        raise ScraperError("Could not extract price from the page")
        
    except Exception as e:
        logger.error(f"Error parsing HTML or extracting price: {e}")
        raise ScraperError(f"HTML parsing error: {e}")


## def origgy():
def scrape_oil_price():
    
    """
    Scrape the oil price from the target website.
    
    Returns:
        Decimal: The extracted oil price as a Decimal
        
    Raises:
        ScraperError: If there are issues with the request or parsing
    """
    
    try:
        logger.info(f"Sending request to {TARGET_URL}")
        response = requests.get(TARGET_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve data from {TARGET_URL}: {e}")
        raise ScraperError(f"Network request failed: {e}")

    
    try:
        ## original code from getpdo.py
        ## target page
        ## pdo = "https://patriotdiscountoil.com/"

        ## call get method to request target page
        pdo_pg = requests.get(TARGET_URL)

        ## lets make soup !!
        soup = BeautifulSoup(pdo_pg.content, "html.parser")

        ## set the search text
        ## srch_text = "Today’s Oil Price"

        ## 
        ## THIS IS WHAT WE ARE SEARCHING FOR 
        ## 
        ##		<div class="elementor-widget-container">
        ##							Today’s Oil Price<br>3.32<sup>9</sup> /gal						</div>
        ##				</div>
        ## 
        ## search by text with the help of the lambda function (?)
        ## find all tags named div and return text inside
        ## works  
        ## findit = soup.find_all(lambda tag: tag.name == "div" and  srch_text in tag.text)
        ## works  
        now=datetime.now()
        ## for item in soup.find(lambda tag: tag.name == "div" and  srch_text in tag.text):
        for item in soup.find(lambda tag: tag.name == "div" and  PRICE_IDENTIFIER in tag.text):
            ## if(srch_text in item.text ):    
            if(PRICE_IDENTIFIER in item.text ):    
                ## WORKS stubby=re.findall("Today’s Oil Price[0-9.]+",item.text ) 
                ## Found Today's Oil Price
                pdo_price=re.findall("[0-9.]+",item.text ) 
                ## Pull out the price
                the_price=pdo_price[0]
                ## print("PDO Price: "+ the_price) 
                print(f'Date: {now:%Y%m%d}, PDO Price: {the_price}')

                logger.info(f"Date: {now:%Y%m%d}, Found price: ${the_price}")
                return extract_and_validate_price(the_price)

        # If we reach here, we couldn't find the price
        logger.error("Price pattern not found near the identifier")
        raise ScraperError("Could not extract price from the page")
        
    except Exception as e:
        logger.error(f"Error parsing HTML or extracting price: {e}")
        raise ScraperError(f"HTML parsing error: {e}")


def extract_and_validate_price(price_text):
    """
    Extract and validate a price from text.
    
    Args:
        price_text (str): The text containing the price
        
    Returns:
        Decimal: The validated price as a Decimal
        
    Raises:
        ScraperError: If the price is invalid or cannot be extracted
    """
    try:
        # Remove currency symbols, commas, and whitespace
        clean_text = re.sub(r'[^\d.]', '', price_text)
        
        # Convert to Decimal for precise handling
        price = Decimal(clean_text)
        
        # Basic validation - ensure the price is reasonable
        if price <= 0 or price > 10:  # Assuming price is in dollars per gallon
            logger.warning(f"Extracted price {price} seems outside reasonable range")
        
        return price
    except (ValueError, InvalidOperation) as e:
        logger.error(f"Failed to convert '{price_text}' to a valid price: {e}")
        raise ScraperError(f"Price validation error: {e}") 