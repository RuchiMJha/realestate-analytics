import duckdb
import os

DB_PATH = os.path.join("data", "processed", "real_estate.db")
CSV_PATH = os.path.join("data", "raw", "realtor-data.csv")

def run_etl():
    print("Connecting to DuckDB...")
    con = duckdb.connect(DB_PATH)
    
    # 1. Create a clean staging schema/table
    print("Creating cleaned staging table...")
    
    con.execute("""
        CREATE OR REPLACE TABLE properties AS
        SELECT DISTINCT
            brokered_by,
            status,
            CAST(price AS DOUBLE) AS price,
            CAST(bed AS INTEGER) AS bed,
            CAST(bath AS INTEGER) AS bath,
            CAST(acre_lot AS DOUBLE) AS acre_lot,
            city,
            state,
            zip_code,
            CAST(house_size AS DOUBLE) AS house_size,
            TRY_CAST(prev_sold_date AS DATE) AS prev_sold_date
        FROM read_csv_auto(?, header=True, types={'prev_sold_date': 'VARCHAR'})
        WHERE price IS NOT NULL 
          AND price > 10000 
          AND (bed IS NULL OR bed > 0)
          AND (bath IS NULL OR bath > 0)
          AND state IS NOT NULL
    """, [CSV_PATH])
    
    # 2. Get some quick validation metrics
    total_rows = con.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
    print(f"ETL Complete! Successfully loaded {total_rows:,} clean records into the database.")
    
    # Show top states by volume to verify spatial distribution
    print("\nTop 5 States by listing volume in your DB:")
    state_summary = con.execute("""
        SELECT state, COUNT(*) as listings, ROUND(AVG(price), 2) as avg_price 
        FROM properties 
        GROUP BY state 
        ORDER BY listings DESC 
        LIMIT 5
    """).df()
    print(state_summary)
    
    con.close()

if __name__ == "__main__":
    run_etl()