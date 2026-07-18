# High-Performance Real Estate Analytics Pipeline

An end-to-end data engineering and analytics pipeline processing over **2.1 Million rows** of real estate market data. This system implements dynamic text-override schema parsing, resilient data cleaning, robust statistical outlier boundaries ($Mean \pm 3\sigma$), and microsecond analytical querying using an embedded DuckDB engine connected to an interactive Streamlit user interface.

## 🔑 Core Technical Highlights

* **High-Volume Analytical Processing:** Utilized DuckDB to execute complex aggregated queries on over 2 million records locally in-memory under 15 milliseconds, bypassing memory bottlenecks inherent in traditional Pandas workflows.
* **Resilient Schema Engineering:** Resolved type conversion exceptions during chunked ingest by implementing structured manual string overrides (`VARCHAR`) mapped to dynamic `TRY_CAST` data types.
* **Data Quality Rigor:** Addressed noisy data entry errors by establishing statistical thresholds using Standard Deviation, stripping invalid listings, and preserving 99.6% structural data integrity.
* **Production Architecture:** Structured completely as an importable Python module with automated linting and syntax checks powered by a GitHub Actions CI/CD workflow.

## 🛠️ Pipeline Architecture

```text
[Raw Realtor CSV Data] 
       |
       v (Resilient Ingestion & VARCHAR Overrides)
[src/ingest_data.py] --> Stores into --> [DuckDB Local Instance]
                                                |
                                                v (Mean + 3*StdDev Filter)
                                       [v_dashboard_properties View]
                                                |
                                                v (Live Parameterized SQL)
                                       [Streamlit Interactive App]



## 📂 Project Structure

realestate-analytics-pipeline/
├── .github/workflows/
│   └── python-app.yml
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── analyze_data.py
│   ├── app.py
│   └── ingest_data.py
├── .gitignore
├── README.md
└── requirements.txt

## 🚀 Quick Start & Installation

1. **Clone the repository and initialize the virtual environment:**
   ```bash
   git clone https://github.com/RuchiMJha/realestate-analytics.git
   cd realestate-analytics-pipeline
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Run the pipeline stages sequentially:
Bash
# Phase 1: Ingest, clean, and deduplicate raw data
python src/ingest_data.py

# Phase 2: Compute statistical ceilings and database views
python src/analyze_data.py

# Phase 3: Spin up the dynamic analytics dashboard
streamlit run src/app.py
📊 Analytical Takeaways & Discoveries
Outlier Pruning: The raw dataset contained extreme anomalies (e.g., empty lots erroneously labeled as properties with millions of square feet of living space). Applying a Mean+3σ threshold systematically isolated and stripped out roughly 7,600 structural data corruptions while cleanly retaining valid high-end real estate listings.
Database Optimization: By migrating from traditional memory-heavy DataFrame filtering to embedded SQL Views inside DuckDB, dashboard query latency dropped from seconds to virtually instantaneous updates, providing a production-grade user experience.
