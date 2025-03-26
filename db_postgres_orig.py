"""
PostgreSQL operations for storing oil price data.
"""
import logging
from datetime import date, datetime
# from decimal import Decimal

import psycopg2
from psycopg2 import sql

## from .config import (
from config import (
    PG_USER, PG_PASS, PG_SERVER, PG_PORT, PG_DATABASE,
    MAIN_TABLE, TEST_TABLE
)

logger = logging.getLogger(__name__)

class PostgresError(Exception):
    """Exception raised for errors in PostgreSQL operations."""
    pass

def get_connection():
    """
    Get a connection to the PostgreSQL database.
    
    Returns:
        connection: A PostgreSQL connection object
        
    Raises:
        PostgresError: If connection cannot be established
    """
    logger.info(f"get_connection: user = {PG_USER}, passwd={PG_PASS}, host={PG_SERVER},  port={PG_PORT}, database={PG_DATABASE}")

    
    try:
        connection = psycopg2.connect(
            user=PG_USER,
            password=PG_PASS,
            host=PG_SERVER,
            port=int(PG_PORT),  # Ensure the port is an integer
            database=PG_DATABASE
        )
        return connection
    except Exception as e:
        logger.error(f"get_connection: Failed to connect to PostgreSQL: {e}")
        raise PostgresError(f"Database connection error: {e}")

def ensure_tables_exist():
    """
    Ensure the required tables exist in PostgreSQL.
    
    Returns:
        None
        
    Raises:
        PostgresError: If there are issues with database operations
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        ## for table_name in [MAIN_TABLE, TEST_TABLE]:
        ##     cursor.execute(f"""
        ##         CREATE TABLE IF NOT EXISTS {table_name} (
        ##             date DATE PRIMARY KEY,
        ##             price DECIMAL(10,3),
        ##             tmstmp TIMESTAMP
        ##         )
        ##     """)
        ##     logger.info(f"Ensured table {table_name} exists in PostgreSQL")
        ##
        ## conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"ensure_tables_exist: Error ensuring PostgreSQL tables: {e}")
        raise PostgresError(f"Database setup error: {e}")

def store_price(price_value, current_date=None, test_mode=False):
    """
    Store the oil price in PostgreSQL.
    
    Args:
        price_value (Decimal): The oil price to store
        current_date (date, optional): The date for the price record. Defaults to today.
        test_mode (bool, optional): Whether to use the test table. Defaults to False.
        
    Returns:
        bool: True if successful
        
    Raises:
        PostgresError: If there are issues with database operations
    """
    if current_date is None:
        current_date = date.today()
    
    timestamp = datetime.now()
    table_name = TEST_TABLE if test_mode else MAIN_TABLE
    logger.info(f"PGSQL: INSERT INTO {table_name} (date, price, tmstmp) VALUES ({current_date}, {price_value}, {timestamp})")
       
    try:
        # Ensure tables exist
        ensure_tables_exist()
        
        # Connect to PostgreSQL
        conn = get_connection()
        cursor = conn.cursor()
        
        logger.info("PGSQL: before select count() ")
        ## MAP: THIS IS CAUSING AN ERROR !! 
        # Check if record exists for this date
        cursor.execute(
            sql.SQL("SELECT COUNT(*) FROM {} WHERE date = %s").format(sql.Identifier(table_name)), 
            [current_date]
        )
        result = cursor.fetchone()
        
        if result[0] > 0:
            # Update existing record
            logger.info(f"PGSQL: UPDATE {table_name} ")
            cursor.execute(
                sql.SQL("UPDATE {} SET price = %s, tmstmp = %s WHERE date = %s").format(sql.Identifier(table_name)),
                [price_value, timestamp, current_date]
            )
            logger.info(f"store_price: Updated price {price_value} for {current_date} in PostgreSQL {table_name}")
        else:
            # Insert new record
            logger.info(f"PGSQL: INSERT {table_name} ")
            cursor.execute(
                sql.SQL("INSERT INTO {} (date, price, tmstmp) VALUES (%s, %s, %s)").format(sql.Identifier(table_name)),
                [current_date, price_value, timestamp]
            )
            logger.info(f"store_price: Inserted price {price_value} for {current_date} in PostgreSQL {table_name}")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error storing price in PostgreSQL: {e}")
        raise PostgresError(f"Database operation error: {e}") 