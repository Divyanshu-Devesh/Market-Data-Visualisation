import io
import json
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, Response, redirect
import pandas as pd

app = Flask(__name__)

# --- GENERIC TELEMETRY LOG GENERATOR (FOR DEMO/DEFAULT RUNS) ---
def generate_mock_telemetry_data():
    platforms = ["Google Ads", "Meta Ads", "LinkedIn Campaign Studio", "TikTok Business", "YouTube Brand Engine"]
    sentiments = ["Strong Positive", "Neutral/Inquisitive", "Frictional/Mixed", "Highly Motivated"]
    topics = ["Enterprise Scalability", "Pricing / ROAS Validation", "Feature Depth Request", "Integration API Setup"]
    stages = ["Impression", "Click-Through", "Lead Generation", "Cart Addition", "Conversion Checkout"]
    
    records = []
    base_time = datetime.now() - timedelta(days=30)
    
    for i in range(120):
        timestamp = (base_time + timedelta(hours=i * 6)).strftime("%Y-%m-%dT%H:%M:%S")
        platform = random.choice(platforms)
        spend = round(random.uniform(150, 2400), 2)
        roas = round(random.uniform(1.2, 6.8), 2)
        revenue = round(spend * roas, 2)
        conversions = random.randint(5, 80)
        cpa = round(spend / conversions, 2) if conversions > 0 else 0
        infra_cost = round(spend * random.uniform(0.02, 0.07), 2)
        
        records.append({
            "timestamp": timestamp,
            "platform": platform,
            "ad_spend": spend,
            "revenue_generated": revenue,
            "roas": roas,
            "conversions": conversions,
            "cpa": cpa,
            "total_infra_cost": infra_cost,
            "funnel_stage": random.choice(stages),
            "sentiment": random.choice(sentiments),
            "intent_topic": random.choice(topics)
        })
    return pd.DataFrame(records)

# Global in-memory storage holding the operating dataframe
CURRENT_DATAFRAME = generate_mock_telemetry_data()

def calculate_executive_summary(df):
    """Generates structured KPI totals and weights safely parsing columns."""
    try:
        total_spend = round(df["ad_spend"].sum(), 2)
        total_revenue = round(df["revenue_generated"].sum(), 2)
        blended_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0
        
        total_conversions = df["conversions"].sum()
        blended_cpa = round(total_spend / total_conversions, 2) if total_conversions > 0 else 0
        total_infra = round(df["total_infra_cost"].sum(), 2)
    except Exception:
        total_spend, total_revenue, blended_roas, blended_cpa, total_infra = 0, 0, 0, 0, 0

    return {
        "total_spend": f"{total_spend:,.2f}",
        "total_revenue": f"{total_revenue:,.2f}",
        "blended_roas": f"{blended_roas:.2f}",
        "blended_cpa": f"{blended_cpa:.2f}",
        "total_infra_cost": f"{total_infra:,.2f}"
    }

@app.route("/")
def dashboard():
    global CURRENT_DATAFRAME
    summary = calculate_executive_summary(CURRENT_DATAFRAME)
    data_records = CURRENT_DATAFRAME.to_dict(orient="records")
    return render_template("dashboard.html", summary=summary, data=data_records)

@app.route("/ingest", methods=["POST"])
def ingest_telemetry():
    """Asynchronous pipeline parsing drag & dropped files."""
    global CURRENT_DATAFRAME
    if "file" not in request.files:
        return jsonify({"error": "Missing valid file attachment form metadata."}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty selection received."}), 400

    if file and file.filename.endswith(".csv"):
        try:
            df = pd.read_csv(file.stream)
            
            # Match schema or fallback to default safely
            required_cols = ["timestamp", "platform", "ad_spend", "revenue_generated", "roas", "conversions", "cpa"]
            for col in required_cols:
                if col not in df.columns:
                    return jsonify({"error": f"Missing required column structure: {col}"}), 400
            
            CURRENT_DATAFRAME = df
            return jsonify({
                "summary": calculate_executive_summary(df),
                "data": df.to_dict(orient="records")
            })
        except Exception as e:
            return jsonify({"error": f"File Parse Failure: {str(e)}"}), 500
            
    return jsonify({"error": "Invalid file type. Only CSV allowed."}), 400

@app.route("/export/csv")
def export_ledger():
    """Generates an immediate runtime download action of current operations."""
    global CURRENT_DATAFRAME
    csv_string = CURRENT_DATAFRAME.to_csv(index=False)
    return Response(
        csv_string,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=marketing_telemetry_ledger.csv"}
    )

import os

if __name__ == "__main__":
    # Keep the environment variable for Render, but change the local default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
