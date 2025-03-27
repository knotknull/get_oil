"""
DuckDB operations for storing oil price data.
"""
import logging
import os
from datetime import date, datetime
# from decimal import Decimal

import duckdb

## from .config import DDB_FULL_PATH, MAIN_TABLE, TEST_TABLE
from config import DDB_FULL_PATH, MAIN_TABLE, TEST_TABLE
from db_sqllog import  log_sql

logger = logging.getLogger(__name__)

class DuckDBError(Exception):
    """Exception raised for errors in DuckDB operations."""
    pass

def ensure_db_exists():
    """
    Ensure the DuckDB database exists and has the required tables.
    
    Returns:
        None
        
    Raises:
        DuckDBError: If there are issues with database operations
    """
    try:
        # Create parent directory if it doesn't exist
        db_dir = os.path.dirname(DDB_FULL_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created directory: {db_dir}")
        
        # Connect to DuckDB
        conn = duckdb.connect(DDB_FULL_PATH)
        
        ## # Create tables if they don't exist
        ## for table_name in [MAIN_TABLE, TEST_TABLE]:
        ##     conn.execute(f"""
        ##         CREATE TABLE IF NOT EXISTS {table_name} (
        ##             date DATE PRIMARY KEY,
        ##             price DECIMAL(10,3),
        ##             tmstmp TIMESTAMP
        ##         )
        ##     """)
        ##     logger.info(f"Ensured table {table_name} exists in DuckDB")
        
        conn.close()
    except Exception as e:
        logger.error(f"Error ensuring DuckDB setup: {e}")
        raise DuckDBError(f"Database setup error: {e}")

def store_price(price_value, current_date=None, test_mode=False):
    """
    Store the oil price in DuckDB.
    
    Args:
        price_value (Decimal): The oil price to store
        current_date (date, optional): The date for the price record. Defaults to today.
        test_mode (bool, optional): Whether to use the test table. Defaults to False.
        
    Returns:
        bool: True if successful
        
    Raises:
        DuckDBError: If there are issues with database operations
    """
    if current_date is None:
        current_date = date.today()
    
    timestamp = datetime.now()
    table_name = TEST_TABLE if test_mode else MAIN_TABLE
   
    logger.info(f"DDB_SQL: INSERT INTO {table_name} (date, price, tmstmp) VALUES ({current_date}, {price_value}, {timestamp}")
    
    try:
        # Ensure database exists
        # ensure_db_exists()
        
        # Connect to DuckDB
        conn = duckdb.connect(DDB_FULL_PATH)
        
        # Check if record exists for this date
        result = conn.execute(
            f"SELECT COUNT(*) FROM {table_name} WHERE date = ?", 
            [current_date]
        ).fetchone()
        
        if result[0] > 0:
            # Update existing record
            conn.execute(
                f"UPDATE {table_name} SET price = ?, tmstmp = CURRENT_TIMESTAMP WHERE date = ?",
                [float(price_value), current_date]
            )
            logger.info(f"Updated price {price_value} for {current_date} in DuckDB {table_name}")
            log_sql("duckdb", f"UPDATE {table_name} SET price = {price_value}, tmstmp = CURRENT_TIMESTAMP WHERE date = {current_date}")
        else:
            # Insert new record
            conn.execute(
                f"INSERT INTO {table_name} (date, price, CURRENT_TIMESTAMP) VALUES (?, ?, ?)",
                [current_date, float(price_value) ]
            )
            logger.info(f"Inserted price {price_value} for {current_date} in DuckDB {table_name}")
            log_sql("duckdb", f"INSERT INTO  {table_name}  (date, price, tmstmp) VALUE ({current_date}, {price_value}, {timestamp})") 
        
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error storing price in DuckDB: {e}")
        raise DuckDBError(f"Database operation error: {e}") 