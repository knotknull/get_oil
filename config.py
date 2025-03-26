"""
Configuration settings for oil price scraper.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Website configuration
TARGET_URL = "https://patriotdiscountoil.com/"
## PRICE_IDENTIFIER = "Today's Oil Price"
##        srch_text = "Today’s Oil Price"
PRICE_IDENTIFIER  = "Today’s Oil Price"


# SQL LOG
SQL_LOG_PATH = os.getenv("SQL_LOG_PATH", ".")

# DuckDB configuration
DDB_PATH = os.getenv("DDB_PATH", ".")
DDB_TBL = os.getenv("DDB_TBL", ".")
DDB_FILENAME = "pdo_prices.ddb"
DDB_FULL_PATH = os.path.join(DDB_PATH, DDB_FILENAME)

# PostgreSQL configuration
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_SERVER = os.getenv("PG_SERVER", "localhost")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_DATABASE = os.getenv("PG_DATABASE")

# Table names - same for both databases
MAIN_TABLE = "pdo_prices"
TEST_TABLE = "test_prices"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") 