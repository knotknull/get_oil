#!/usr/bin/env python3
"""
Main application script for the home heating oil price scraper.

This script scrapes oil prices from the target website and stores them
in both DuckDB and PostgreSQL databases.
"""
import argparse
import logging
# import os
import sys
from datetime import date

from scraper import scrape_oil_price, ScraperError
from db_duckdb import store_price as store_price_duckdb, DuckDBError
from db_ddb2pg import store_price as store_price_postgres, PGDuckDBError
from config import LOG_FORMAT, LOG_LEVEL, PG_USER, PG_PASS, PG_DATABASE, DDB_PATH, DDB_TBL

# Set up logger
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_environment():
    """
    Check if all required environment variables are set.
    
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    required_vars = {
        'DDB_PATH': DDB_PATH,
        'DDB_TBL': DDB_TBL,
    }
    
    # PostgreSQL variables are only required if --duckdb-only is not specified
    args = sys.argv
    if '--duckdb-only' not in args:
        required_vars.update({
            'PG_USER': PG_USER,
            'PG_PASS': PG_PASS,
            'PG_DATABASE': PG_DATABASE
        })
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file")
        return False
    
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Scrape and store home heating oil prices.')
    parser.add_argument('--test', action='store_true', help='Use test tables for storage')
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format (defaults to today)')
    parser.add_argument('--duckdb-only', action='store_true', help='Store in DuckDB only')
    parser.add_argument('--postgres-only', action='store_true', help='Store in PostgreSQL only')
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    # Check environment variables before proceeding
    if not check_environment():
        return 1
        
    args = parse_args()
    
    # Determine which databases to use
    use_duckdb = not args.postgres_only
    use_postgres = not args.duckdb_only
    
    # Parse date if provided
    current_date = None
    if args.date:
        try:
            current_date = date.fromisoformat(args.date)
        except ValueError:
            logger.error(f"Invalid date format: {args.date}. Expected YYYY-MM-DD format.")
            return 1
    
    # Set test mode flag
    test_mode = args.test
    
    # Log startup information
    logger.info("Starting home heating oil price scraper")
    logger.info(f"Test mode: {test_mode}")
    logger.info(f"Date: {current_date if current_date else 'Today'}")
    logger.info(f"Using DuckDB: {use_duckdb}")
    logger.info(f"Using PostgreSQL: {use_postgres}")
    
    try:
        # Scrape oil price from website
        price = scrape_oil_price()
        logger.info(f"Successfully scraped oil price: {price}")
        
        # Store in DuckDB if enabled
        if use_duckdb:
            try:
                store_price_duckdb(price, current_date, test_mode)
                logger.info("Successfully stored in DuckDB")
            except DuckDBError as e:
                logger.error(f"DuckDB storage failed: {e}")
                return 1
        
        # Store in PostgreSQL if enabled
        if use_postgres:
            try:
                store_price_postgres(price, current_date, test_mode)
                logger.info("Successfully stored in PostgreSQL")
            except PGDuckDBError as e:
                logger.error(f"PostgreSQL storage failed: {e}")
                return 1
        
        logger.info("Oil price scraper completed successfully")
        return 0
    
    except ScraperError as e:
        logger.error(f"Scraper error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 