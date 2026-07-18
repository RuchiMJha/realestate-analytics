import duckdb
import os

DB_PATH = os.path.join("data", "processed", "real_estate.db")

def clean_outliers():
    con = duckdb.connect(DB_PATH)
    print("Connected to DuckDB. Analyzing anomalies...")
    
    # 1. Calculate statistical thresholds for price and house size
    stats = con.execute("""
        SELECT 
            AVG(price) as avg_p, 
            STDDEV(price) as std_p,
            AVG(house_size) as avg_s,
            STDDEV(house_size) as std_s
        FROM properties
        WHERE house_size IS NOT NULL
    """).fetchone()
    
    avg_p, std_p, avg_s, std_s = stats
    price_upper_bound = avg_p + (3 * std_p)
    size_upper_bound = avg_s + (3 * std_s)
    
    print(f"Price statistical ceiling (Mean + 3 StdDev): ${price_upper_bound:,.2f}")
    print(f"Size statistical ceiling (Mean + 3 StdDev): {size_upper_bound:,.2f} sq ft")
    
    # 2. Create a clean View for our dashboard to read from
    con.execute(f"""
        CREATE OR REPLACE VIEW v_dashboard_properties AS
        SELECT * 
        FROM properties
        WHERE price <= {price_upper_bound}
          AND (house_size IS NULL OR house_size <= {size_upper_bound})
    """)
    
    dashboard_rows = con.execute("SELECT COUNT(*) FROM v_dashboard_properties").fetchone()[0]
    print(f"Created analytical view 'v_dashboard_properties' with {dashboard_rows:,} outlier-free listings.")
    
    con.close()

if __name__ == "__main__":
    clean_outliers()