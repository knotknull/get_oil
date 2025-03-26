import duckdb

# Connect to the DuckDB database
con = duckdb.connect('data.ddb')

# Read the first five rows of the table xyz_data
print("First five rows of xyz_data:")
result = con.execute("SELECT * FROM xyz_data LIMIT 5").fetchall()
for row in result:
    print(row)

# Insert a new record into the xyz_data table
new_record = ('2025-02-26', 4.123, '2025-02-26 12:00:00')
con.execute("INSERT INTO xyz_data (date, price, tmstmp) VALUES (?, ?, ?)", new_record)

# Verify the insertion
print("\nAfter insertion:")
result = con.execute("SELECT * FROM xyz_data ORDER BY date DESC LIMIT 5").fetchall()
for row in result:
    print(row)

# Close the connection
con.close()