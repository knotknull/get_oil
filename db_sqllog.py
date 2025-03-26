"""
SQL Log ogoperations to store the SQL that was used saving data 
"""
import logging
import os
from datetime import datetime
from config import SQL_LOG_PATH
logger = logging.getLogger(__name__)


def log_sql(db_name, sql_string):
    """
    Write a SQL string to the SQL log file with a timestamp.
    
    Args:
        db_name (str): The datbase that the SQL was run against .
        sql_string (str): The SQL string to log.
        
    Returns:
        None
    """
    try:
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(SQL_LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        sqllog=SQL_LOG_PATH + db_name + ".sql.log"        
        # Append the SQL string to the log file with a timestamp
        with open(sqllog, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {sql_string}\n")
        
        logger.info(f"Logged SQL to {SQL_LOG_PATH}: {sql_string}")
    except Exception as e:
        logger.error(f"Error logging SQL: {e}")
        raise
