#initializes our local database file and runs a super-fast analytical lookup directly against the raw CSV file without ever loading it entirely into RAM.
import duckdb
import os

# Define database path
DB_PATH = os.path.join("data", "processed", "real_estate.db")
CSV_PATH = os.path.join("data", "raw", "realtor-data.csv")

print("Initializing DuckDB database...")
con = duckdb.connect(DB_PATH)

# Using DuckDB's fast CSV reader to scan the first 5 rows and verify it reads perfectly
print("Previewing raw CSV data via SQL...")
preview = con.execute(f"SELECT * FROM read_csv_auto('{CSV_PATH}') LIMIT 5").df()
print(preview)

con.close()
print("Database initialized successfully!")
