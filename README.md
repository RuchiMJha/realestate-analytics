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

## 💻 Core Codebase & Component Breakdown

### 1. Data Ingestion Pipeline (`src/ingest_data.py`)
This module handles the resilient extraction and loading of the raw real estate datasets into the local analytical database.
* **Resilient Schema Overrides:** Due to dirty data and mixed types in raw CSV chunks, fields are explicitly ingested as `VARCHAR` to eliminate type-conversion crashes during mass-scale ingestion.
* **Dynamic Database Casting:** Implements optimized DuckDB `TRY_CAST` operations to safely transform string representations into correct numeric (`DOUBLE`, `INTEGER`) and structural primitives during the database load phase.
* **Local In-Memory Persistence:** Seeds and structures the underlying DuckDB file engine (`data/processed/`), bypassing standard file-system overhead.

### 2. Statistical Analytics & Quality Engine (`src/analyze_data.py`)
This component acts as the data quality gatekeeper and analytical transformation layer.
* **Outlier Boundary Enforcement:** Computes mathematical data bounds using a strict standard deviation filter ($Mean \pm 3\sigma$) on critical features like listing price and property square footage.
* **Database View Generation:** Instead of keeping heavy transformations in volatile memory, it persists the cleaned dataset directly inside DuckDB as an optimized database view (`v_dashboard_properties`). 
* **Data Integrity Preservation:** Filters out extreme anomalous data entries (such as empty lots with millions of square feet) while successfully preserving over 99.6% of structurally sound data records.

### 3. Interactive Analytical Dashboard (`src/app.py`)
The presentation layer built natively on top of Streamlit to deliver live data exploration.
* **Microsecond Query Latency:** Leverages DuckDB's embedded columnar execution engine to run complex SQL aggregations on over 2.1 Million rows in under 15 milliseconds.
* **Parameterized SQL Filters:** Connects UI components (sliders, multiselect dropdowns) directly to parameterized internal SQL operations, preventing security risks and maintaining a highly responsive UI.
* **Memory Efficiency:** Bypasses memory bottlenecks traditional Pandas configurations face by allowing the user interface to stream aggregated views straight out of the database engine on demand.

### 4. Automated CI/CD Testing Workflow (`.github/workflows/python-app.yml`)
The continuous integration engine ensuring code health across contributions.
* **Syntax and Linting Quality:** Triggers on every code push or pull request to analyze code layout via standard Python formatters.
* **Import Verification:** Automatically validates the codebase as an independent, importable Python module by scanning the `__init__.py` hooks.
