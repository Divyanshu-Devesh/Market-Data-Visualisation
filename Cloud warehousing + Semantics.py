import os
import sqlite3
import pandas as pd
import duckdb
import plotly.express as px
from datetime import datetime

# =====================================================================
# 1. CLOUD WAREHOUSE CONNECTOR / SIMULATOR
# =====================================================================
class CloudDataWarehouse:
    """
    Manages connections and execution inside the Cloud Data Warehouse (e.g., Snowflake).
    Implements a local fallback engine (DuckDB) for zero-setup execution.
    """
    def __init__(self, use_live_snowflake=False):
        self.use_live = use_live_snowflake
        if self.use_live:
            import snowflake.connector
            self.conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA")
            )
        else:
            # Local high-performance analytical engine simulating Snowflake SQL syntax
            self.conn = duckdb.connect(database=':memory:')
            self._seed_mock_warehouse()

    def _seed_mock_warehouse(self):
        """Seeds the warehouse raw staging schema with marketing data."""
        raw_data = pd.DataFrame([
            {"date": "2026-05-10", "campaign_id": "C001", "channel": "Google Ads", "spend": 450.00, "clicks": 600, "conversions": 30},
            {"date": "2026-05-10", "campaign_id": "C002", "channel": "Meta Ads", "spend": 150.00, "clicks": 400, "conversions": 8},
            {"date": "2026-05-11", "campaign_id": "C001", "channel": "Google Ads", "spend": 500.00, "clicks": 750, "conversions": 45},
            {"date": "2026-05-11", "campaign_id": "C002", "channel": "Meta Ads", "spend": 155.00, "clicks": 380, "conversions": 5},
            {"date": "2026-05-12", "campaign_id": "C001", "channel": "Google Ads", "spend": 600.00, "clicks": 900, "conversions": 60},
            {"date": "2026-05-12", "campaign_id": "C002", "channel": "Meta Ads", "spend": 200.00, "clicks": 510, "conversions": 12},
        ])
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        self.conn.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
        self.conn.register("raw_marketing_data", raw_data)
        self.conn.execute("CREATE TABLE raw.stg_marketing_metrics AS SELECT * FROM raw_marketing_data")

    def execute_query(self, query: str):
        """Executes a query and returns results as a Pandas DataFrame."""
        if self.use_live:
            return pd.read_sql(query, self.conn)
        else:
            return self.conn.execute(query).df()

# =====================================================================
# 2. TRANSFORMATION LAYER (dbt Style Cloud Views)
# =====================================================================
def run_warehouse_transformations(dw: CloudDataWarehouse):
    """
    Simulates a dbt run inside the Cloud Warehouse.
    Creates clean downstream tables and models optimized for semantic consumption.
    """
    print("[dbt Transformation] Building analytics.fct_marketing_performance...")
    
    # Cloud SQL script consolidating dimensions and granular facts
    dbt_model_sql = """
    CREATE OR REPLACE TABLE analytics.fct_marketing_performance AS 
    SELECT 
        CAST(date AS DATE) as metric_date,
        UPPER(channel) as marketing_channel,
        campaign_id,
        CAST(spend AS DOUBLE) as spend,
        CAST(clicks AS INTEGER) as clicks,
        CAST(conversions AS INTEGER) as conversions
    FROM raw.stg_marketing_metrics;
    """
    # Adjust for DuckDB syntax variants during mock testing
    if not dw.use_live:
        dbt_model_sql = dbt_model_sql.replace("CREATE OR REPLACE TABLE", "CREATE TABLE")
        
    dw.conn.execute(dbt_model_sql)
    print("[dbt Transformation] Transformation complete. Downstream analytical views ready.")

# =====================================================================
# 3. THE SEMANTIC LAYER (Metrics Definition Engine)
# =====================================================================
class SemanticLayerEngine:
    """
    Acts as the single source of truth for metrics (like Looker LookML or Cube).
    Guarantees that formulas like CAC or ROAS are never hardcoded in downstream dashboards.
    """
    def __init__(self, dw: CloudDataWarehouse):
        self.dw = dw
        # Programmatic representation of a semantic YAML configuration
        self.cube_definition = {
            "cube": "marketing_performance",
            "dimensions": ["metric_date", "marketing_channel"],
            "measures": {
                "total_spend": "SUM(spend)",
                "total_clicks": "SUM(clicks)",
                "total_conversions": "SUM(conversions)",
                # Derived/Calculated metrics defined dynamically at query time
                "cac": "SUM(spend) / NULLIF(SUM(conversions), 0)",
                "cpc": "SUM(spend) / NULLIF(SUM(clicks), 0)"
            }
        }

    def query_metric(self, measures: list, dimensions: list, filters: str = ""):
        """
        Compiles semantic dimensions & measures dynamically into strict Data Warehouse SQL.
        """
        # Parse measures from semantic dictionary definitions
        measure_exprs = [f"{self.cube_definition['measures'][m]} AS {m}" for m in measures]
        select_fields = dimensions + measure_exprs
        
        select_clause = ", ".join(select_fields)
        group_clause = ", ".join([str(i+1) for i in range(len(dimensions))])
        
        where_clause = f"WHERE {filters}" if filters else ""
        
        # Construct exact warehouse dialect SQL compilation
        compiled_sql = f"""
        SELECT {select_clause}
        FROM analytics.fct_marketing_performance
        {where_clause}
        GROUP BY {group_clause}
        ORDER BY {dimensions[0]} ASC
        """
        
        print(f"\n[Semantic Engine] Compiled SQL Sent to Cloud Data Warehouse:\n{compiled_sql}")
        return self.dw.execute_query(compiled_sql)

# =====================================================================
# 4. MODERN VISUALIZATION LAYER
# =====================================================================
def render_dashboard(semantic_data: pd.DataFrame, metric_name: str):
    """Generates an executive-level analytical plot using Semantic data feeds."""
    fig = px.line(
        semantic_data,
        x="metric_date",
        y=metric_name,
        color="marketing_channel",
        title=f"Marketing Efficiency Tracking: {metric_name.upper()} Over Time",
        labels={"metric_date": "Date", metric_name: metric_name.upper()},
        markers=True,
        template="plotly_dark"
    )
    fig.show()

# =====================================================================
# PIPELINE ORCHESTRATION
# =====================================================================
if __name__ == "__main__":
    print("--- Initialization of Cloud Stack Pipeline ---")
    
    # Connect to Warehouse (Toggle to True if env variables are ready)
    warehouse = CloudDataWarehouse(use_live_snowflake=False)
    
    # Run transformations (dbt Simulation)
    run_warehouse_transformations(warehouse)
    
    # Instantiate the Semantic Layer Schema
    semantic_layer = SemanticLayerEngine(warehouse)
    
    # BI Tool requests performance metrics via Semantic layer API 
    # instead of writing dirty SQL or modifying data frames locally!
    print("\n--- BI Dashboard Fetching via Semantic Layer ---")
    marketing_kpis = semantic_layer.query_metric(
        measures=["total_spend", "cac", "cpc"],
        dimensions=["metric_date", "marketing_channel"]
    )
    
    print("\n--- Resulting Semantic Layer Normalized DataFrame ---")
    print(marketing_kpis)
    
    # Render modern visual asset
    render_dashboard(marketing_kpis, metric_name="cac")

    print("\n--- Pipeline Run Successfully Executed ---")