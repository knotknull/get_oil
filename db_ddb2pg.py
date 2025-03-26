"""
PostgreSQL operations for storing oil price data.
"""
import logging
# import os
from datetime import date, datetime
# from decimal import Decimal

import duckdb

from config import MAIN_TABLE, TEST_TABLE
from db_sqllog import  log_sql

logger = logging.getLogger(__name__)

class PGDuckDBError(Exception):
    """Exception raised for errors in PGDuckDB operations."""
    pass


def ensure_db_exists():
    """
    Ensure the ddb to pgsql database exists and has the required tables.
    
    Returns:
        None
        
    Raises:
        PGDuckDBError: If there are issues with database operations
    """
    ## table_name = TEST_TABLE if test_mode else MAIN_TABLE
    try:
        
        # Connect to DuckDB to PGSQL
        con = duckdb.connect()  
        ## con.sql(f"""
        ##     INSTALL postgres;
        ##     LOAD postgres;  
        ##     ATTACH '' as pgsql_pdo (TYPE postgres, SECRET pgsql_pdo, SCHEMA 'public');
        ## """)
        con.sql("""
            INSTALL postgres;
            LOAD postgres;  
            ATTACH '' as pgsql_pdo (TYPE postgres, SECRET pgsql_pdo, SCHEMA 'public');
        """)
        result = con.execute ("  SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'").fetchall()
        logger.info(f"ensure_db_exists: connectected to pgsql: {result} ")
        con.close()
    except Exception as e:
        logger.error(f"Error ensuring DuckDB setup: {e}")
        raise PGDuckDBError(f"Database setup error: {e}")

def store_price(price_value, current_date=None, test_mode=False):
    """
    Store the oil price in PostgreSQL via DuckDB.
    
    Args:
        price_value (Decimal): The oil price to store
        current_date (date, optional): The date for the price record. Defaults to today.
        test_mode (bool, optional): Whether to use the test table. Defaults to False.
        
    Returns:
        bool: True if successful
        
    Raises:
        PGDuckDBError: If there are issues with database operations
    """
    if current_date is None:
        current_date = date.today()
    
    timestamp = datetime.now()
    table_name = TEST_TABLE if test_mode else MAIN_TABLE
   
    logger.info(f"PGSQL: INSERT INTO {table_name} (date, price, tmstmp) VALUES ({current_date}, {price_value}, {timestamp}")
    
    try:
        # Ensure database exists
        # ensure_db_exists()
        
        # Connect to DuckDB
        con = duckdb.connect()  
        ## con.sql(f"""
        ##     INSTALL postgres;
        ##     LOAD postgres;  
        ##     ATTACH '' as pgsql_pdo (TYPE postgres, SECRET pgsql_pdo, SCHEMA 'public');
        ## """)
        con.sql("""
            INSTALL postgres;
            LOAD postgres;  
            ATTACH '' as pgsql_pdo (TYPE postgres, SECRET pgsql_pdo, SCHEMA 'public');
        """)
       
        
        # Check if record exists for this date
        result = con.execute(
            f"SELECT COUNT(*) FROM pgsql_pdo.{table_name} WHERE date = ?", 
            [current_date]
        ).fetchone()
        ## result = con.execute( f"SELECT COUNT(*) FROM pgsql_pdo.{table_name}", ).fetchone()
        
        if result[0] > 0:
            # Update existing record
            con.execute(
                f"UPDATE pgsql_pdo.{table_name} SET price = ?, tmstmp = ? WHERE date = ?",
                [float(price_value), timestamp, current_date]
            )
            logger.info(f"Updated price {price_value} for {current_date} in PosgreSQL pgsql_pdo.{table_name}")
            log_sql("pgsql", f"UPDATE {table_name} SET price = {price_value}, tmstmp = {timestamp} WHERE date = {current_date}")

        else:
            # Insert new record
            con.execute(
                f"INSERT INTO pgsql_pdo.{table_name} (date, price, tmstmp) VALUES (?, ?, ?)",
                [current_date, float(price_value), timestamp]
            )
            logger.info(f"Inserted price {price_value} for {current_date} in PosgreSQL pgsql_pdo.{table_name}")
            log_sql("pgsql", f"INSERT INTO  {table_name}  (date, price, tmstmp) VALUE (?, ?, ?)",  
                    [current_date, float(price_value), timestamp])
            
        con.close()
        return True
    except Exception as e:
        logger.error(f"Error storing price in DuckDB: {e}")
        raise PGDuckDBError(f"Database operation error: {e}") 
    