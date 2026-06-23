import os
import sqlite3
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. API EXTRACTION (Mocking Google Ads API)
# ==========================================
def extract_marketing_data():
    """
    Simulates fetching daily performance metrics from a Marketing API.
    In production, you would use requests.get(API_URL, headers=headers) 
    or the official google-ads Python SDK.
    """
    print("Extracting data from Marketing API...")
    
    # Simulating API JSON response payload
    mock_api_response = [
        {"date": "2026-05-10", "campaign": "Summer_Sale_US", "spend": 450.00, "impressions": 12000, "clicks": 600, "conversions": 30},
        {"date": "2026-05-10", "campaign": "Brand_Awareness_EU", "spend": 150.00, "impressions": 25000, "clicks": 400, "conversions": 8},
        {"date": "2026-05-11", "campaign": "Summer_Sale_US", "spend": 500.00, "impressions": 14000, "clicks": 750, "conversions": 45},
        {"date": "2026-05-11", "campaign": "Brand_Awareness_EU", "spend": 150.00, "impressions": 22000, "clicks": 380, "conversions": 5},
        {"date": "2026-05-12", "campaign": "Summer_Sale_US", "spend": 600.00, "impressions": 18000, "clicks": 900, "conversions": 60},
        {"date": "2026-05-12", "campaign": "Brand_Awareness_EU", "spend": 200.00, "impressions": 30000, "clicks": 510, "conversions": 12},
        {"date": "2026-05-13", "campaign": "Summer_Sale_US", "spend": 550.00, "impressions": 16500, "clicks": 820, "conversions": 50},
        {"date": "2026-05-13", "campaign": "Brand_Awareness_EU", "spend": 180.00, "impressions": 28000, "clicks": 460, "conversions": 10}
    ]
    
    return pd.DataFrame(mock_api_response)

# ==========================================
# 2. TRANSFORMATION (Data Cleaning & Calc)
# ==========================================
def transform_marketing_data(df):
    """
    Cleans the data and calculates core performance marketing KPIs:
    CTR (Click-Through Rate), CPC (Cost Per Click), and ROAS / CPA foundations.
    """
    print("Transforming data and calculating KPIs...")
    
    # Ensure proper data types
    df['date'] = pd.to_datetime(df['date'])
    df['spend'] = df['spend'].astype(float)
    
    # Calculate Custom Marketing Metrics
    # CTR = Clicks / Impressions
    df['ctr'] = (df['clicks'] / df['impressions']) * 100
    
    # CPC = Spend / Clicks (handle division by zero if any)
    df['cpc'] = df['spend'] / df['clicks']
    df['cpc'] = df['cpc'].fillna(0)
    
    # Cost per Conversion (CPA) = Spend / Conversions
    df['cpa'] = df['spend'] / df['conversions']
    df['cpa'] = df['cpa'].fillna(0)
    
    # Add a pipeline timestamp
    df['updated_at'] = datetime.now()
    
    return df

# ==========================================
# 3. LOADING (Staging to Data Warehouse)
# ==========================================
def load_to_warehouse(df, db_name="marketing_warehouse.db"):
    """
    Loads the transformed dataframe into a local SQLite database acting as our warehouse.
    Uses 'append' mode to simulate continuous daily pipeline runs.
    """
    print(f"Loading data into warehouse ({db_name})...")
    conn = sqlite3.connect(db_name)
    
    # Save to SQL table
    df.to_sql("fact_marketing_performance", conn, if_exists="replace", index=False)
    conn.close()
    print("Database load complete.")

# ==========================================
# 4. VISUALIZATION (Modern Interactive BI)
# ==========================================
def create_dashboard(db_name="marketing_warehouse.db"):
    """
    Queries the database and builds modern interactive visualizations 
    using Plotly to track campaign efficiency.
    """
    print("Fetching data from warehouse for visualization...")
    conn = sqlite3.connect(db_name)
    df = pd.read_sql("SELECT * FROM fact_marketing_performance", conn)
    conn.close()
    
    # Visualization 1: Spend vs Conversions over time
    print("Generating Campaign Performance Chart...")
    fig_perf = px.line(
        df, 
        x="date", 
        y="conversions", 
        color="campaign",
        title="Daily Conversions by Campaign",
        labels={"date": "Date", "conversions": "Conversions Converted"},
        markers=True,
        template="plotly_dark"  # Modern dark mode theme
    )
    fig_perf.show()
    
    # Visualization 2: Cost Per Conversion (CPA) Efficiency Matrix
    fig_cpa = px.bar(
        df,
        x="campaign",
        y="cpa",
        color="campaign",
        barmode="group",
        title="Average Cost per Conversion (Lower = More Efficient)",
        labels={"cpa": "CPA ($)"},
        template="plotly_dark"
    )
    fig_cpa.show()

# ==========================================
# RUNNING THE PIPELINE
# ==========================================
if __name__ == "__main__":
    print("--- Starting Modern Marketing ETL Pipeline ---")
    
    # Step 1: Extract
    raw_data = extract_marketing_data()
    
    # Step 2: Transform
    transformed_data = transform_marketing_data(raw_data)
    
    # Step 3: Load
    load_to_warehouse(transformed_data)
    
    # Step 4: Visualize
    create_dashboard()
    
    print("--- Pipeline Execution Finished Successfully ---")