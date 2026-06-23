from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import numpy as np
import io

app = FastAPI(title="AI Marketing Intelligence Architecture System")
templates = Jinja2Templates(directory="templates")

def generate_high_fidelity_marketing_data():
    """Generates a complete, granular data framework matching all 9 core metrics."""
    np.random.seed(42)
    rows = 50
    
    platforms = ["Meta Ads", "Google Search", "TikTok Ads", "LinkedIn Campaign", "YouTube Video"]
    intents = ["Product Pricing", "Feature Inquiry", "Competitor Comparison", "Integration Tech", "Enterprise Sales"]
    sentiments = ["Positive", "Neutral", "Urgent Inquiry"]
    funnel_stages = ["Impression", "Click-Through", "Lead Generation", "Cart Addition", "Conversion Checkout"]
    
    df = pd.DataFrame({
        "timestamp": pd.date_range(end=pd.Timestamp.now(), periods=rows, freq="12h").strftime("%Y-%m-%d %H:%M"),
        "platform": np.random.choice(platforms, size=rows),
        "intent_topic": np.random.choice(intents, size=rows),
        "sentiment": np.random.choice(sentiments, size=rows, p=[0.5, 0.3, 0.2]),
        "funnel_stage": np.random.choice(funnel_stages, size=rows),
        "ad_spend": np.random.uniform(200, 1500, size=rows).round(2),
        "revenue_generated": np.random.uniform(400, 6000, size=rows).round(2),
        "conversions": np.random.randint(5, 80, size=rows),
        "clicks": np.random.randint(100, 2000, size=rows),
        "llm_prompt_cost": np.random.uniform(0.01, 0.04, size=rows).round(4),
        "llm_completion_cost": np.random.uniform(0.02, 0.09, size=rows).round(4),
    })
    
    # Calculate downstream KPI fields dynamically
    df["roas"] = (df["revenue_generated"] / df["ad_spend"]).round(2)
    df["cpa"] = (df["ad_spend"] / df["conversions"]).round(2)
    df["total_llm_cost"] = df["llm_prompt_cost"] + df["llm_completion_cost"]
    return df

CURRENT_DATA_POOL = generate_high_fidelity_marketing_data()

@app.get("/", response_class=HTMLResponse)
async def serve_actionable_dashboard(request: Request):
    global CURRENT_DATA_POOL
    df = CURRENT_DATA_POOL.copy()
    
    # Calculate executive summary overview metrics
    total_spend = df["ad_spend"].sum()
    total_rev = df["revenue_generated"].sum()
    blended_roas = round(total_rev / total_spend, 2) if total_spend > 0 else 0
    blended_cpa = round(total_spend / df["conversions"].sum(), 2) if df["conversions"].sum() > 0 else 0
    total_infra_cost = df["total_llm_cost"].sum()
    
    summary_framework = {
        "total_spend": f"{total_spend:,.2f}",
        "total_revenue": f"{total_rev:,.2f}",
        "blended_roas": blended_roas,
        "blended_cpa": blended_cpa,
        "total_infra_cost": round(total_infra_cost, 4),
        "total_records": len(df)
    }
    
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "summary": summary_framework,
            "data": df.to_dict(orient="records")
        }
    )

@app.post("/upload-telemetry")
async def handle_data_migration(file: UploadFile = File(...)):
    global CURRENT_DATA_POOL
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        CURRENT_DATA_POOL = df
        return JSONResponse(content={"status": "Data Lake Synced", "records": len(df)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "Fault", "detail": str(e)})

@app.get("/export/csv")
async def export_warehouse_csv():
    global CURRENT_DATA_POOL
    stream = io.StringIO()
    CURRENT_DATA_POOL.to_csv(stream, index=False)
    response = StreamingResponse(io.BytesIO(stream.getvalue().encode()), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=comprehensive_marketing_export.csv"
    return response

@app.post("/query")
async def sandbox_query(payload: dict):
    return JSONResponse(content={"status": "Success", "pipeline_output_extract": "AI Core operational pipeline tracking stable."})