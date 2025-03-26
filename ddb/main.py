
import os
import duckdb
from dotenv import load_dotenv

def load_env_vars():
    # load env vars from .env
    load_dotenv()
    
    # Load all environment variables into a dictionary
    env_vars = {key: os.getenv(key) for key in os.environ.keys()}
    return env_vars

def test_duckdb(ddb_file, tbl):
    # Connect to the DuckDB database
    qry=f"SELECT * FROM {tbl} LIMIT 2"
    print("qry: ", qry) 
    with duckdb.connect(ddb_file) as con:
        result = con.execute(qry).fetchall()
        for row in result: 
            print(row)
        # con.sql(qry"SELECT * from pdo_prices LIMIT 2;")
        # result = con.execute(qry, [tbl])
        # for row in result.fectchall():
        #     print(row)
        # the context manager closes the connection
    

def insert_price(ddb_file, tbl, dt, prc):
    # Connect to the DuckDB database
    qry=f""" INSERT INTO {tbl} (date, price, tmstmp)
            VALUES ('{dt}', {prc}, current_localtimestamp())
            ON CONFLICT (date) DO UPDATE SET price = EXCLUDED.price, tmstmp = EXCLUDED.tmstmp;
    """
      
    print("qry: ", qry) 
    
    with duckdb.connect(ddb_file) as con:
        result = con.execute(qry)
        print(result.rowcount, "record(s) inserted.")
        
        
##MAP # Connect to the DuckDB database
##MAP con = duckdb.connect('data.ddb')
##MAP 
##MAP # Read the first five rows of the table xyz_data
##MAP print("First five rows of xyz_data:")
##MAP result = con.execute("SELECT * FROM xyz_data LIMIT 5").fetchall()
##MAP for row in result:
##MAP     print(row)
##MAP 
##MAP # Insert a new record into the xyz_data table
##MAP new_record = ('2025-02-26', 4.123, '2025-02-26 12:00:00')
##MAP con.execute("INSERT INTO xyz_data (date, price, tmstmp) VALUES (?, ?, ?)", new_record)
##MAP 
##MAP # Verify the insertion
##MAP print("\nAfter insertion:")
##MAP result = con.execute("SELECT * FROM xyz_data ORDER BY date DESC LIMIT 5").fetchall()
##MAP for row in result:
##MAP     print(row)
##MAP 
##MAP # Close the connection
##MAP con.close()
def getdata():
    # Load environmental variables from .env
    load_dotenv()
    
    ddb_data = os.getenv("DDB_DATA") 
    tbl_nm  = os.getenv("DDB_TBL") 
    test_duckdb(ddb_data, tbl_nm)

    ## Date: 20250225, PDO Price: 3.339
    insert_price(ddb_data, tbl_nm, '2025-02-25', "3.339")

def main():
    print("Hello from ddb!")

    getdata()


if __name__ == "__main__":
    main()
