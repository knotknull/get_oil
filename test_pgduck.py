import duckdb  

con = duckdb.connect()  
con.sql("""
    INSTALL postgres;
    LOAD postgres;  
    ATTACH '' as pgsql_pdo (TYPE postgres, SECRET pgsql_pdo, SCHEMA 'public');
""")

result = con.execute ("  SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'").fetchall()
print(result)        


con.sql("select * from pgsql_pdo.pdo_prices where date = '2025-03-25';").show()
con.sql("select * from pgsql_pdo.test_prices where date = '2025-03-25';").show()
table_name="pgsql_pdo.pdo_prices"
result = con.execute(
            f"SELECT COUNT(*) FROM {table_name} WHERE date = ?", 
            ['2025-03-25']
        ).fetchone()
print(result)        