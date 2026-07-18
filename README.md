# High-Performance Real Estate Analytics Pipeline

An end-to-end data engineering and analytics pipeline processing over **2.1 Million rows** of real estate market data. This system implements dynamic text-override schema parsing, resilient data cleaning, robust statistical outlier boundaries ($Mean \pm 3\sigma$), and microsecond analytical querying using an embedded DuckDB engine connected to an interactive Streamlit user interface.

## 🔑 Core Technical Highlights

* **High-Volume Analytical Processing:** Utilized DuckDB to execute complex aggregated queries on over 2 million records locally in-memory under 15 milliseconds, bypassing memory bottlenecks inherent in traditional Pandas workflows.
* **Resilient Schema Engineering:** Resolved type conversion exceptions during chunked ingest by implementing structured manual string overrides (`VARCHAR`) mapped to dynamic `TRY_CAST` data types.
* **Data Quality Rigor:** Addressed noisy data entry errors by establishing statistical thresholds using Standard Deviation, stripping invalid listings, and preserving 99.6% structural data integrity.
* **Production Architecture:** Structured completely as an importable Python module with automated linting and syntax checks powered by a GitHub Actions CI/CD workflow.
## 🛠️ Pipeline Architecture

<pre>
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
</pre>

## 📂 Project Structure

<pre>
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
</pre>
